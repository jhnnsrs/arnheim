from typing import Any, Callable, Awaitable, Dict

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from bioconverter.serializers import BioImageSerializer
from importer.models import Importer
from importer.serializers import ImportingSerializer
from importer.utils import *
from larvik.consumers import LarvikError, ModelFuncAsyncLarvikConsumer, SyncLarvikConsumer, TypedSyncLarvikConsumer
from larvik.discover import register_consumer
from django.conf import settings

import os
from larvik.models import LarvikJob

FILES_ROOT = settings.FILES_ROOT


@register_consumer("importer", model= Importer)
class ImportingConsumer(TypedSyncLarvikConsumer[Importing]):
    name = "Home Importer"
    path = "HomeImporter"
    settings = {"reload": True}
    inputs = [Locker, "Creator"]
    outputs = [BioImage]
    requestClass = Importing


    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": None}


    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Importing": ImportingSerializer,
            "BioImage": BioImageSerializer,
        }

    def start(self, request: Importing, settings: dict):
        creator: User = request.creator
        locker = request.locker

        # Media Path of Nginx is solely MEDIA, this one here is /code/media

        base_dir = os.path.join(FILES_ROOT, creator.username)
        self.progress(base_dir)
        self.progress("Starting")

        self.progress( os.listdir(base_dir))
        filelist = [(filename, os.path.join(base_dir, filename)) for filename in os.listdir(base_dir)]

        if len(filelist) == 0: raise LarvikError("No Files in directory.")

        self.logger.info("Files To Import {0}".format(filelist))
        # %%
        progress = self.progress
        updateModel = self.updateModel
        # %%
        def moveFileToLocker(path, name):

            if os.path.exists(path):
                progress("Moving file " + path)

                directory = "{0}/{1}/".format(request.creator.id, request.locker.id)
                directory = os.path.join(BIOIMAGE_ROOT, directory)

                if not os.path.exists(directory):
                    os.makedirs(directory)

                new_path = os.path.join(directory, os.path.basename(name))
                shutil.move(path, new_path)

                name = name if name else os.path.basename(path)
                image = BioImage.objects.create(file=new_path,
                                                creator=request.creator,
                                                locker=request.locker,
                                                name=os.path.basename(name),
                                                nodeid= request.nodeid)

                image.save()
                updateModel(image, "created")
                return image

        bioimages = []

        for file in filelist:
            path = file[1]
            name = file[0]
            bioimages.append((moveFileToLocker(path, name), "create"))


        self.progress("Done")

        return {"BioImage": filelist}








