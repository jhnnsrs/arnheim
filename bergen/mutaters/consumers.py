from typing import Dict, Any, Callable, Awaitable

import numpy as np
from django.db import models
from rest_framework import serializers

from larvik.consumers import AsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.utils import update_status_on_larvikjob
from mutaters.models import Mutating, Mutater, Reflection
from mutaters.serializers import ReflectionSerializer, MutatingSerializer
from mutaters.utils import get_mutating_or_error, reflection_update_or_create
from elements.models import Transformation
from trontheim.consumers import OsloJobConsumer


class MutatingOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startconverting(self, data):
        await self.register(data)
        print(data)
        request: Mutating = await get_mutating_or_error(data["data"])
        self.request = request
        settings: dict = await self.getsettings(request.settings, request.mutater.defaultsettings)

        array = request.transformation.numpy.get_array()

        file = await self.convert(array, settings)

        func = self.getDatabaseFunction()
        model, method = await func(request, file)

        await self.modelCreated(model, self.getSerializer(), method)

    async def convert(self, settings: dict, array: np.array):
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




@register_consumer("imagemutater", model= Mutater)
class ImageMutator(AsyncLarvikConsumer):
    name = "Image Mutater"
    path = "Image Mutater"
    settings = {"reload": True}
    inputs = [Transformation]
    outputs = [Reflection]

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_mutating_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return { "image": reflection_update_or_create}

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return { "Mutating": MutatingSerializer,
                 "Reflection": ReflectionSerializer}

    async def parse(self, request: Mutating, settings: dict) -> Dict[str, Any]:
        array = request.transformation.numpy.get_array()

        # TODO: Maybe faktor this one out
        if len(array.shape) == 5:
            array = np.nanmax(array[:, :, :3, :, 0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:, :, :3, :], axis=3)
        if len(array.shape) == 3:
            array = array[:, :, :3]
            if array.shape[2] == 1:
                x = array[:, :, 0]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3))

                # do expand
                target[:x.shape[0], :x.shape[1], 0] = x

                array = target
            if array.shape[2] == 2:
                x = array[:, :, :1]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3))

                # do expand
                target[:x.shape[0], :x.shape[1], :1] = x

                array = target
        if len(array.shape) == 2:
            x = array[:, :]

            # expand to what shape
            target = np.zeros((array.shape[0], array.shape[1], 3))

            # do expand
            target[:x.shape[0], :x.shape[1], 0] = x

            array = target

        self.logger.info("Output image has shape {0}".format(array.shape))
        img = None # TODO: Impelemnt
        return {"image": img }

