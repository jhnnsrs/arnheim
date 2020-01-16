from typing import Dict, Any, Callable, Awaitable

import bioformats
import javabridge as javabridge
from django.db import models
from rest_framework import serializers

from bioconverter.logic.bioparser import getSeriesNamesFromFile
from biouploader.models import Analyzing
from biouploader.serializers import BioSeriesSerializer, AnalyzingSerializer
from biouploader.utils import get_analyzing_or_error, bioseries_create_or_update
from larvik.consumers import LarvikConsumer, ModelFuncAsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from larvik.utils import update_status_on_larvikjob

javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

@register_consumer("biometa")
class BioAnalyzer(ModelFuncAsyncLarvikConsumer):

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

        seriesnames = getSeriesNamesFromFile(filepath)
        bioseries = []
        for index, seriesname in enumerate(seriesnames):
            bioseries.append({"name": seriesname, "index": index})

        await self.progress("Database Action Files")
        return {"BioSeries": bioseries}




