from rest_framework import serializers

from larvik.discover import register_consumer
from trontheim.consumers import OsloJobConsumer
from visualizers.models import Visualizing
from visualizers.serializers import ProfileSerializer, VisualizingSerializer, ExcelExportSerializer
from visualizers.utils import get_visualizing_or_error, update_profile_or_create, update_status_on_visualizing, \
    update_excelexport_or_create


class VisualizingOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startconverting(self, data):
        await self.register(data)
        print(data)
        request: Visualizing = await get_visualizing_or_error(data["data"])
        self.request = request

        # WORKING ON
        request = await update_status_on_visualizing(request, "WORKING")
        await self.modelCreated(request, VisualizingSerializer, "update")

        settings: dict = await self.getsettings(request.settings, request.visualizer.defaultsettings)

        try:
            returnvalues = await self.convert(request, settings)

            func = self.getDatabaseFunction()
            model, method = await func(request, settings, returnvalues)

            await self.modelCreated(model, self.getSerializer(), method)

            request = await update_status_on_visualizing(request, "DONE")
            await self.modelCreated(request, VisualizingSerializer, "update")
        except Exception as e:
            print(e)
            request = await update_status_on_visualizing(request, e)
            await self.modelCreated(request, VisualizingSerializer, "update")




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


@register_consumer("profiler")
class Profiler(VisualizingOsloJob):

    def getDatabaseFunction(self):
        return update_profile_or_create

    def getSerializer(self):
        return ProfileSerializer

    async def convert(self, request: Visualizing, conversionsettings: dict):
        # TODO: Maybe faktor this one out
        dataframe = request.answer.pandas.get_dataframe()
        print("Creating Profile")
        report = dataframe.profile_report(title=request.answer.name, style={'full_width': True})

        return report


@register_consumer("excel")
class ExcelExporter(VisualizingOsloJob):

    def getDatabaseFunction(self):
        return update_excelexport_or_create

    def getSerializer(self):
        return ExcelExportSerializer

    async def convert(self, request: Visualizing, conversionsettings: dict):
        # TODO: Maybe faktor this one out
        dataframe = request.answer.pandas.get_dataframe()

        return dataframe
