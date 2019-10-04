from django.contrib.auth.models import User
from rest_framework import serializers

from biouploader.serializers import BioImageSerializer
from importer.models import Importing
from importer.serializers import ImportingSerializer
from mandal.settings import FILES_ROOT
from trontheim.consumers import OsloJobConsumer
from visualizers.models import Visualizing
from visualizers.serializers import ProfileSerializer, VisualizingSerializer, ExcelExportSerializer
from importer.utils import *
import pandas_profiling

class ImportingOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def updateStatus(self,status):
        self.request = await update_status_on_request(self.request, status)
        return await self.modelCreated(self.request, self.getRequestSerializer(), "update")

    def getRequestSerializer(self):
        return ImportingSerializer


    async def startconverting(self, data):
        await self.register(data)
        print(data)
        request: Importing = await get_importing_or_error(data["data"])
        self.request = request

        if not self.request.locker: self.request = update_importing_with_new_Locker(self.request)

        # WORKING ON
        await self.updateStatus("WORKING")

        settings: dict = await self.getsettings(self.request.settings, self.request.importer.defaultsettings)

        try:
            returnvalues = await self.convert(self.request, settings)

            func = self.getDatabaseFunction()
            createdList = await func(self.request, settings, returnvalues)

            for item in createdList:
                await self.modelCreated(item[0], self.getSerializer(), item[1])

            await self.updateStatus("DONE")
        except Exception as e:
            print(e)
            await self.updateStatus(e)




    async def convert(self, request: Visualizing, settings: dict):
        """ If you create objects make sure you are handling them in here
        and publish if necessary with its serializer """
        raise NotImplementedError

    def getDatabaseFunction(self):
        """ This should update the newly generated model, will get called with the request and the convert"""
        raise NotImplementedError

    def getSerializer(self) -> serializers.ModelSerializer:
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



class Importer(ImportingOsloJob):

    def getDatabaseFunction(self):
        return create_bioimages_from_list

    def getSerializer(self):
        return BioImageSerializer

    async def convert(self, request: Importing, conversionsettings: dict):
        # TODO: Maybe faktor this one out
        creator: User = request.creator
        locker = request.locker

        # Media Path of Nginx is solely MEDIA, this one here is /code/media

        import os
        base_dir = os.path.join(FILES_ROOT,creator.username)

        filelist = [(filename, os.path.join(base_dir, filename)) for filename in os.listdir(base_dir)]
        print("Files To Import" ,filelist)
        # %%

        return filelist


