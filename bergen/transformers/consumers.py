import json
from typing import Dict, Any, Callable, Awaitable

import numpy as np
from django.db import models
from rest_framework import serializers

from larvik.consumers import LarvikConsumer, update_status_on_larvikjob, LarvikError
from transformers.logic.linerectifier_logic import translateImageFromLine
from transformers.models import Transforming
from transformers.serializers import TransformationSerializer, TransformingSerializer
from transformers.utils import get_transforming_or_error, outputtransformation_update_or_create


# import the logging library


class LineRectifierTransformer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_transforming_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:

        return { "array" : outputtransformation_update_or_create}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:

        return {
            "Transforming": TransformingSerializer,
            "Transformation": TransformationSerializer,
        }

    async def parse(self, request: Transforming, settings: dict) -> Dict[str, Any]:
        array = request.representation.numpy.get_array()
        roi = request.roi
        vectors = json.loads(roi.vectors)

        vertices = [[key["x"], key["y"]] for key in vectors]

        self.logger.info("Array has max of {0}".format(array.max()))
        array = np.float64(array)

        await self.progress(10, message="Converting array")
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, settings.get("scale",10))

        return {"array": image}


class SliceLineTransformer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_transforming_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:

        return {"array": outputtransformation_update_or_create}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:

        return {
            "Transforming": TransformingSerializer,
            "Transformation": TransformationSerializer,
        }


    async def parse(self, request: Transforming, settings: dict) -> Dict[str, Any]:

        rep = request.representation
        roi = request.roi
        shape = json.loads(rep.shape)
        z_size = shape[3]


        vectors = json.loads(roi.vectors)

        vertices = [[key["x"],key["y"]] for key in vectors]

        scale = settings.get("scale",10)
        # We Have to Slice the Array first in order to make the transformation work
        lowerBound1: int = settings.get("lower", 0)
        upperBound1: int = settings.get("upper", z_size - 1)

        if upperBound1 is None: raise LarvikError("Upper Bound Not correctly set")
        if lowerBound1 is None: raise LarvikError("Lower Bound Not correctly set")

        if lowerBound1 > upperBound1:
            lowerBound = upperBound1
            upperBound = lowerBound1
        else:
            lowerBound = lowerBound1
            upperBound = upperBound1

        await self.progress(20,message="Getting array from file system")
        array = rep.numpy.get_z_bounded_array(lowerBound,upperBound)

        self.logger.info("Collection Array of Shape {0} ".format(array.shape))
        self.logger.info("With Vertices like {0}".format(vertices))
        self.logger.info("Scale: {0}".format(scale))

        if len(array.shape) == 5:
            array = np.nanmax(array[:, :, :3, :, 0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:, :, :3, :], axis=3)
        if len(array.shape) == 3:
            array = array[:, :, :3]
        if len(array.shape) == 2:
            array = array[:, :]

        await self.progress(60, message="Transforming")
        self.logger.info("Maxed array of shape {0}".format(array.shape))
        array = np.float64(array)
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(scale))


        return { "array" : image }
