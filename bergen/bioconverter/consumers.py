import javabridge as javabridge
import bioformats
import numpy as np
import nibabel as nib
from channels.consumer import AsyncConsumer

from bioconverter.models import ConversionRequest, Conversing
from bioconverter.utils import get_inputmodel_or_error, \
    update_outputrepresentation_or_create, update_sample_with_meta, create_sample_or_override, get_conversing_or_error, \
    get_sample_or_error
from biouploader.models import BioImage, BioSeries
from chat.logic.bioparser import loadSeriesFromFile
from drawing.models import Sample
from drawing.serializers import SampleSerializer
from filterbank.addins import toimage
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer
from trontheim.consumers import OsloJobConsumer



class ConvertBioSeriesOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    async def convertseries(self, data):
        await self.register(data)
        print(data)
        request: Conversing = await get_conversing_or_error(data["data"])
        sample, method = await create_sample_or_override(request)
        settings: dict = await self.getsettings(request.settings, request.converter.defaultsettings)
        bioseries: BioSeries = request.bioserie
        sample_id: int = sample.id

        convertedarray, meta = await self.convert(settings, bioseries)

        sample, method2 = await update_sample_with_meta(sample_id, meta)
        outputrep, method = await update_outputrepresentation_or_create(request, sample, convertedarray, meta)
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


javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)


class BioConverter(ConvertBioSeriesOsloJob):
    async def convert(self, settings: dict, bioseries: BioSeries):
        filepath = bioseries.bioimage.file.path

        meta, array = loadSeriesFromFile(filepath, bioseries.index)

        return array, meta


