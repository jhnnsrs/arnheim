from typing import Any, Callable, Awaitable, Dict

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from bioconverter.serializers import BioImageSerializer
from importer.models import Importer
from importer.serializers import ImportingSerializer
from importer.utils import *
from larvik.consumers import LarvikError, ModelFuncAsyncLarvikConsumer
from larvik.discover import register_consumer
from mandal.settings import FILES_ROOT


class ImportingConsumer(ModelFuncAsyncLarvikConsumer):

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo":True}

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_importing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_request

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model], Awaitable[Any]]]:
        return {
            "BioImage": create_bioimages_from_list
        }

    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Importing": ImportingSerializer,
            "BioImage": BioImageSerializer,
        }

    async def parse(self, request: models.Model, settings: dict) -> Dict[str, Any]:
       raise NotImplementedError




@register_consumer("importer", model= Importer, )
class Importer(ImportingConsumer):
    name = "Home Importer"
    path = "HomeImporter"
    settings = {"reload": True}
    inputs = [Locker, "Creator"]
    outputs = [BioImage]

    async def parse(self, request: Importing, settings: dict):
        # TODO: Maybe faktor this one out
        creator: User = request.creator
        locker = request.locker

        # Media Path of Nginx is solely MEDIA, this one here is /code/media

        import os
        base_dir = os.path.join(FILES_ROOT,creator.username)

        await self.progress("0")

        filelist = [(filename, os.path.join(base_dir, filename)) for filename in os.listdir(base_dir)]

        if len(filelist) == 0: raise LarvikError("No Files in directory.")

        self.logger.info("Files To Import {0}".format(filelist))
        # %%
        await self.progress("10")

        return {"BioImage" : filelist }


