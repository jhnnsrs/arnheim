import javabridge as javabridge
import bioformats
import numpy as np
import nibabel as nib
from channels.consumer import AsyncConsumer

from biouploader.models import BioImage, Analyzing, BioSeries
from biouploader.serializers import BioSeriesSerializer
from biouploader.utils import get_analyzing_or_error, update_bioseries_or_create
from chat.logic.bioparser import loadSeriesFromFile, getSeriesNamesFromFile
from drawing.models import Sample
from drawing.serializers import SampleSerializer
from filterbank.addins import toimage
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer
from trontheim.consumers import OsloJobConsumer


class AnalyzeBioImageOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Analyzing = await get_analyzing_or_error(data["data"])
        bioimage: BioImage = request.bioimage

        bioserieslist = await self.analyze(bioimage, request)


        for bioseries in bioserieslist:
            outputbioseries, method = await update_bioseries_or_create(request, bioseries)
            await self.modelCreated(outputbioseries, BioSeriesSerializer, method)

    async def analyze(self, bioimage: BioImage, analyzing: Analyzing):
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


class BioAnalyzer(AnalyzeBioImageOsloJob):
    async def analyze(self,bioimage: BioImage, analyzing: Analyzing):
        filepath = bioimage.file.path
        print("Analyzing Bioimage of locker",bioimage.locker)
        seriesnames =  getSeriesNamesFromFile(filepath)
        bioseries = []
        for index,seriesname in enumerate(seriesnames):
            bioseries.append(BioSeries(name=seriesname, index=index, bioimage = bioimage, nodeid=analyzing.nodeid, locker_id=bioimage.locker_id))

        return bioseries
