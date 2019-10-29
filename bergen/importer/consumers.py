from typing import Any, Callable, Awaitable, Dict

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from biouploader.serializers import BioImageSerializer
from importer.models import Importing
from importer.serializers import ImportingSerializer
from larvik.consumers import LarvikConsumer
from mandal.settings import FILES_ROOT
from trontheim.consumers import OsloJobConsumer
from visualizers.models import Visualizing
from visualizers.serializers import ProfileSerializer, VisualizingSerializer, ExcelExportSerializer
from importer.utils import *
import pandas_profiling


class ImportingConsumer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_importing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_request

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model], Awaitable[Any]]]:
        return {
            "BioImage": create_bioimages_from_list
        }

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Importing": ImportingSerializer,
            "BioImage": BioImageSerializer,
        }

    async def parse(self, request: models.Model, settings: dict) -> Dict[str, Any]:
       raise NotImplementedError



class Importer(ImportingConsumer):

    async def parse(self, request: Importing, conversionsettings: dict):
        # TODO: Maybe faktor this one out
        creator: User = request.creator
        locker = request.locker

        # Media Path of Nginx is solely MEDIA, this one here is /code/media

        import os
        base_dir = os.path.join(FILES_ROOT,creator.username)

        filelist = [(filename, os.path.join(base_dir, filename)) for filename in os.listdir(base_dir)]
        print("Files To Import" ,filelist)
        # %%

        return {"BioImage" : filelist }


