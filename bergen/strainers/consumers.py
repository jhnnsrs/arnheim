from typing import Dict, Any, Callable, Awaitable

import numpy as np
from django.db import models
from rest_framework import serializers

from larvik.consumers import LarvikError, DaskSyncLarvikConsumer, AsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from larvik.utils import update_status_on_larvikjob
from strainers.models import Straining, Strainer
from strainers.serializers import StrainingSerializer
from strainers.utils import get_straining_or_error, outputtransformation_update_or_create
from transformers.models import Transformation
from transformers.serializers import TransformationSerializer


# import the logging library



@register_consumer("intensityprofiler", model= Strainer)
class IntensityProfiler(DaskSyncLarvikConsumer):
    name = "Intensity Profiler"
    path = "Intensity Profiler"
    settings = {"reload": True}
    inputs = [Transformation]
    outputs = [Transformation]

    # TODO: Broken
    def getRequest(self, data) -> LarvikJob:
        return Straining.objects.get(pk=data["id"])

    def getSerializers(self):
        return {"Straining": StrainingSerializer,
                "Transformation": TransformationSerializer
                }

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"parse": True}

    def parse(self, request: Straining, settings: dict) -> Dict[str, Any]:
        print(str(self.c))

        transformation_image = request.transformation.loadArray()
        height = 0
        ndim = 2

        if len(transformation_image.shape) > 3 or len(transformation_image.shape) < 2:
            raise LarvikError("This is not a valid transformation. Shape exceeds the available dimensions")
        if len(transformation_image.shape) == 3:
            height, width, channels = transformation_image.shape
            ndim = 3
        if len(transformation_image.shape) == 2:
            height, width = transformation_image.shape
            channels = 0
            ndim = 2

        # this takes the middle part of the picture
        middleup = int((height / 2) - (height / 4))
        middledown = int((height / 2) + (height / 4))

        # trimm image according to needs
        if ndim == 3:
            trimmedimage = transformation_image[middleup:middledown, :, :]
        else:
            trimmedimage = transformation_image[middleup:middledown, :]

        np.seterr(divide='ignore', invalid='ignore')  # error level if a pixelvalue is 0
        averages = np.max(trimmedimage, axis=0)
        intensity = averages / averages.max(axis=0)
        if "channels" in settings:
            self.logger.info("Original Intensitycurve had shape of {0}".format(intensity.shape))
            selectedchannels = list(map(lambda item: item["value"], settings["channels"]))
            self.logger.info("Selecting Channels {0}".format(selectedchannels))
            intensity = np.take(intensity, selectedchannels, axis=1)
            self.logger.info("Intensitycurves now has shape of {0}".format(intensity.shape))

        return {"array": intensity}




@register_consumer("masker", model= Strainer,)
class Masker(AsyncLarvikConsumer):
    name = "Masker"
    path = "Masker"
    settings = {"reload": True}
    inputs = [Transformation]
    outputs = [Transformation]

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_straining_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return {"array": outputtransformation_update_or_create}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Transformation": TransformationSerializer,
            "Straining": StrainingSerializer
        }

    async def parse(self, request: Straining, settings: dict) -> Dict[str, Any]:

        array = request.transformation.numpy.get_array()

        vec = []
        if "mask" in settings:
            vec = settings["mask"]

        x, y = np.meshgrid(np.arange(array.shape[1]), np.arange(array.shape[0]))
        pix = np.vstack((x.flatten(), y.flatten())).T
        clustermask = np.zeros_like(array[:, :, 0])

        restored = clustermask
        for el in vec:
            restored.flat[el] = 1
        print(restored.shape)

        return {"array": restored}
