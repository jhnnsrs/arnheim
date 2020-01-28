from typing import Dict, Callable, Awaitable

import bioformats
import javabridge
from django.db import models
from rest_framework import serializers

from bioconverter.logic.parsing import convertBioImageToXArray
from bioconverter.models import Conversing, Converter, Representation
from bioconverter.serializers import RepresentationSerializer, ConversingSerializer
from bioconverter.utils import create_sample_or_override, get_conversing_or_error, \
    update_status_on_conversing, update_sample_with_meta2, update_outputrepresentation_or_create2
from biouploader.models import BioSeries
from biouploader.serializers import BioImageSerializer
from elements.models import Sample
from elements.serializers import SampleSerializer
from larvik.consumers import AsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob

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



