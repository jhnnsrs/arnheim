from typing import Dict, Callable, Awaitable, Any

import bioformats
import javabridge
from django.db import models
from rest_framework import serializers

from bioconverter.logic.meta import getSeriesNamesForFile
from bioconverter.logic.parsing import convertBioImageToXArray
from bioconverter.models import Conversing, Converter, Analyzer, BioImage, Analyzing, BioSeries
from bioconverter.serializers import ConversingSerializer, AnalyzingSerializer, \
    BioSeriesSerializer, BioImageSerializer
from bioconverter.utils import create_sample_or_override, get_conversing_or_error, \
    update_status_on_conversing, update_sample_with_meta2, update_outputrepresentation_or_create2, \
    get_analyzing_or_error, bioseries_create_or_update

from elements.models import Sample, Representation
from elements.serializers import SampleSerializer, RepresentationSerializer
from larvik.consumers import AsyncLarvikConsumer, ModelFuncAsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from larvik.utils import update_status_on_larvikjob

javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

class ConverterConsumer(AsyncLarvikConsumer):

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"overwrite":True}

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[LarvikJob]]:
        return get_conversing_or_error


    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_conversing


    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return { "Conversing": ConversingSerializer,
                 "Sample": SampleSerializer,
                 "BioImage": BioImageSerializer,
                 "Representation": RepresentationSerializer}

    async def convert(self,request, settings: Dict):
        raise NotImplementedError

    async def start(self, request: Conversing, settings: Dict):
        sample, method = await create_sample_or_override(request, settings)
        await self.progress("Sample Instatiation")

        try:
            array, meta = await self.convert(request, settings)

            await self.progress("Parsed")
            sample, samplemethod = await update_sample_with_meta2(sample, meta, settings)
            await self.progress(f"{str(samplemethod).capitalize()} Sample {sample.name}")
            await self.updateModel(sample,samplemethod)

            await self.progress("Compressing and Saving")
            rep, repmethod = await update_outputrepresentation_or_create2(request, sample, array, settings)
            await self.updateModel(rep,repmethod)

        except FileNotFoundError as e:
            self.logger.error("File Not Found")


@register_consumer("bioconverter",model = Converter)
class BioConverter(ConverterConsumer):
    name = "Bioconverter"
    path = "BioConverter"
    settings = {"reload": True,
                "overwrite": False}
    inputs = [BioSeries]
    outputs = [Sample, Representation]


    async def parseProgress(self,message):
        await self.progress(message)

    async def convert(self, request, settings: Dict):
        filepath = request.bioserie.bioimage.file.path
        index = request.bioserie.index

        array, parseimagemeta = await convertBioImageToXArray(filepath, index, self.progress)
        return array, parseimagemeta



@register_consumer("biometa", model= Analyzer)
class BioAnalyzer(ModelFuncAsyncLarvikConsumer):
    name = "Biometa"
    path = "BioMeta"
    settings = {"reload": True}
    inputs = [BioImage]
    outputs = [BioSeries]



    def getModelFuncDict(self):
        return { "BioSeries" : bioseries_create_or_update}

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[LarvikJob]]:
        return get_analyzing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Analyzing": AnalyzingSerializer,
            "BioSeries": BioSeriesSerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"overwrite": True}

    async def parse(self, request: Analyzing, settings: dict) -> Dict[str, Any]:
        filepath = request.bioimage.file.path
        self.logger.info("Trying to parse bioimage at Path {0}".format(filepath))
        await self.progress("Opening Files")

        seriesnames = getSeriesNamesForFile(filepath)
        bioseries = []
        for index, seriesname in enumerate(seriesnames):
            bioseries.append({"name": seriesname, "index": index})

        await self.progress("Database Action Files")
        return {"BioSeries": bioseries}




