from typing import Dict, Any, Callable, Awaitable

import numpy as np
import nibabel as nib
from django.db import models
from rest_framework import serializers

from filterbank.logic.addins import toimage
from larvik.consumers import LarvikConsumer, update_status_on_larvikjob, LarvikError
from metamorphers.models import Metamorphing
from metamorphers.serializers import DisplaySerializer, ExhibitSerializer, MetamorphingSerializer
from metamorphers.utils import get_metamorphing_or_error, get_inputrepresentation_or_error, \
    update_exhibit_or_create, update_display_or_create, exhibit_update_or_create
from trontheim.consumers import OsloJobConsumer


class MetamorphingOsloJobConsumer(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startJob(self, data):
        await self.register(data)
        print(data)
        request: Metamorphing = await get_metamorphing_or_error(data["data"])
        self.request = request
        settings: dict = await self.getsettings(request.settings, request.metamorpher.defaultsettings)

        inputrep, array = await get_inputrepresentation_or_error(request)

        file = await self.convert(array, settings)
        if not file: return

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

class NiftiMetamorpher(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_metamorphing_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return {
            "Nifti": exhibit_update_or_create
        }

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Exhibit": ExhibitSerializer,
            "Metamorphing": MetamorphingSerializer,
        }

    async def parse(self, request: Metamorphing, conversionsettings: dict) -> Dict[str, Any]:

        array = request.representation.numpy.get_array()
        self.logger.info("Trying to Metamorph Array of Shape {0}".format(array.shape))

        rescale = conversionsettings.get("rescale",False)
        if len(array.shape) != 5:
            self.logger.info("Not the right shape")

            raise LarvikError("Not the right shape for the job")

        print(array.dtype)
        array = array[:, :, :, :, 0]
        cmin = array.min()
        cmax = array.max()
        high = 255
        low = 0

        cscale = cmax - cmin
        if cscale < 0:
            raise LarvikError("`cmax` should be larger than `cmin`.")
        elif cscale == 0:
            cscale = 1

        scale = float(high - low) / cscale
        if rescale:
            await self.progress(20, message="Interpolating")
            self.logger.info("Interpolatiion of Array from {0} to {1}".format(cmin, cmax))
            array = (array - cmin) * scale + low
            array = (array.clip(low, high) + 0.5).astype("uint8")
        else:
            array = array * 255

        array = array.astype("u1")
        await self.progress(60, message="Swaping Axes")
        array = array.swapaxes(2, 3)
        shape_3d = array.shape[0:3]
        self.logger.info("New Shape is {0}".format(shape_3d))
        rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])

        array = np.ascontiguousarray(array, dtype='u1')
        await self.progress(80, message="Continuing Array")
        array = array.view(rgb_dtype).reshape(shape_3d)
        img1 = nib.Nifti1Image(array, np.eye(4))

        return { "Nifti": img1 }




class ImageMetamorpher(MetamorphingOsloJobConsumer):

    def getDatabaseFunction(self):
        return update_display_or_create

    def getSerializer(self) -> serializers.ModelSerializer:
        return DisplaySerializer

    async def convert(self, array: np.array, conversionsettings: dict):
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
        print(array.shape)
        img = toimage(array)
        return img



