from typing import Dict, Any, Callable, Awaitable

import bioformats
import javabridge as javabridge
from django.db import models
from rest_framework import serializers

from bioconverter.logic.bioparser import getSeriesNamesFromFile
from biouploader.models import Analyzing
from biouploader.serializers import BioSeriesSerializer, AnalyzingSerializer
from biouploader.utils import get_analyzing_or_error, bioseries_create_or_update
from larvik.consumers import LarvikConsumer, update_status_on_larvikjob

javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

class BioAnalyzer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_analyzing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return { "BioSeries" : bioseries_create_or_update}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Analyzing" : AnalyzingSerializer,
            "BioSeries" : BioSeriesSerializer}

    async def parse(self, request: Analyzing, settings: dict) -> Dict[str, Any]:
        filepath = request.bioimage.file.path
        self.logger.info("Trying to parse bioimage at Path {0}".format(filepath))
        await self.progress(10,"Opening Files")
        seriesnames = getSeriesNamesFromFile(filepath)
        bioseries = []
        for index, seriesname in enumerate(seriesnames):
            bioseries.append({ "name":seriesname,"index":index})
        await self.progress(20, "Database Action Files")
        return {"BioSeries" : bioseries }

