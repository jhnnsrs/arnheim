from typing import Dict, Any, Callable, Awaitable

import bioformats
import javabridge as javabridge
from django.db import models
from rest_framework import serializers

from bioconverter.models import Conversing
from bioconverter.utils import update_outputrepresentation_or_create, update_sample_with_meta, \
    create_sample_or_override, get_conversing_or_error, \
    get_sample_or_error, update_status_on_conversing
from biouploader.models import BioSeries
from bioconverter.logic.bioparser import loadSeriesFromFile
from elements.serializers import SampleSerializer
from bioconverter.serializers import RepresentationSerializer, ConversingSerializer
from larvik.consumers import LarvikConsumer
from trontheim.consumers import OsloJobConsumer


class ConvertBioSeriesOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    async def updateStatusOnRequest(self,request,status):
        request = await update_status_on_conversing(request, status)
        print("Updated with message", status)
        await self.modelCreated(request, ConversingSerializer, "update")
        return request

    async def convertseries(self, data):
        await self.register(data)
        print(data)
        request: Conversing = await get_conversing_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.converter.defaultsettings)
        sample, method = await create_sample_or_override(request, settings)
        request = await update_status_on_conversing(request, "Sample instantiation")
        bioseries: BioSeries = request.bioserie
        sample_id: int = sample.id

        request = await update_status_on_conversing(request, "Starting Conversion")
        convertedarray, meta = await self.convert(settings, bioseries)

        sample, method2 = await update_sample_with_meta(sample_id, meta, settings)
        outputrep, method = await update_outputrepresentation_or_create(request, sample, convertedarray, meta, settings)
        await self.modelCreated(outputrep, RepresentationSerializer, method)

        sample = await get_sample_or_error(sample)
        await self.modelCreated(sample, SampleSerializer, "create")

    async def convert(self, settings: dict, bioimage: BioSeries):
        raise NotImplementedError

    async def getsettings(self, settings: str, defaultsettings: str):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = json.loads(defaultsettings)
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings


class ConversionConsumer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_conversing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_conversing

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        pass

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        pass

    async def parse(self, request: models.Model, settings: dict) -> Dict[str, Any]:
        raise NotImplementedError


class BioConverter(ConvertBioSeriesOsloJob):
    async def convert(self, settings: dict, bioseries: BioSeries):
        filepath = bioseries.bioimage.file.path
        print("TRYING THE BEST")
        meta, array = loadSeriesFromFile(filepath, bioseries.index)

        return array, meta


