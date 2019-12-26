import json
from typing import Dict, Any, Callable, Awaitable

import numpy as np
from django.db import models
from rest_framework import serializers

from bioconverter.models import Representation
from drawing.models import ROI
from larvik.consumers import LarvikConsumer, update_status_on_larvikjob, LarvikError, DistributedLarvikConsumer
from strainers.models import Straining
from strainers.serializers import StrainingSerializer
from strainers.utils import get_straining_or_error, update_outputtransformation_or_create, \
    outputtransformation_update_or_create
from transformers.models import  Transformation
from transformers.serializers import TransformationSerializer
from trontheim.consumers import OsloJobConsumer
# import the logging library


class IntensityProfiler(DistributedLarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_straining_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return { "array" : outputtransformation_update_or_create}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Transformation": TransformationSerializer,
            "Straining": StrainingSerializer
        }

    async def parse(self, request: Straining, settings: dict) -> Dict[str, Any]:

        print(str(self.c))

        transformation_image = request.transformation.numpy.get_array()
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


class Masker(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_straining_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return { "array" : outputtransformation_update_or_create}

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






