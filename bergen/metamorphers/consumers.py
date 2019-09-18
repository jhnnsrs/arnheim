from channels.consumer import AsyncConsumer
import numpy as np
import nibabel as nib
from rest_framework import serializers

from filterbank.addins import toimage
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer
from metamorphers.models import Metamorphing
from metamorphers.serializers import DisplaySerializer, ExhibitSerializer
from metamorphers.utils import get_metamorphing_or_error, get_inputrepresentation_or_error, \
    update_nifti_on_representation, update_image_on_representation, update_nifti_on_exhibit, update_image_on_display
from trontheim.consumers import OsloJobConsumer


class MetamorphingOsloJobConsumer(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startconverting(self, data):
        await self.register(data)
        print(data)
        request: Metamorphing = await get_metamorphing_or_error(data["data"])
        self.request = request
        settings: dict = await self.getsettings(request.settings, request.metamorpher.defaultsettings)

        inputrep, array = await get_inputrepresentation_or_error(request)

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



class NiftiMetamorpher(MetamorphingOsloJobConsumer):

    def getDatabaseFunction(self):
        return update_nifti_on_exhibit

    def getSerializer(self) -> serializers.ModelSerializer:
        return ExhibitSerializer

    async def convert(self, array, conversionsettings: dict):
        print(array.shape)
        if len(array.shape) == 5:
            array = array[:, :, :, :, 0]
            if array.shape[2] == 1:
                x = array[:, :, 0, :]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3, array.shape[3]))

                # do expand
                target[:x.shape[0], :x.shape[1], 0, :] = x

                array = target
            elif array.shape[2] == 2:
                x = array[:, :, :1, :]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3, array.shape[3]))

                # do expand
                target[:x.shape[0], :x.shape[1], :1, : ] = x

                array = target
            else:
                array =  array[:,:,:3, :]
        if len(array.shape) == 4:
            array = array[:, :, :, :]
            if array.shape[2] == 1:
                x = array[:, :, 0, :]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3, array.shape[3]))

                # do expand
                target[:x.shape[0], :x.shape[1], 0, :] = x

                array = target
            elif array.shape[2] == 2:
                x = array[:, :, :1,: ]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3, array.shape[3]))

                # do expand
                target[:x.shape[0], :x.shape[1], :1, : ] = x

                array = target
            else:
                array =  array[:,:,:3, :]
        if len(array.shape) == 3:
            array = array[:, :, :]
            if array.shape[2] == 1:
                x = array[:, :, 0]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3,1))

                # do expand
                target[:x.shape[0], :x.shape[1], 0,0] = x

                array = target
            elif array.shape[2] == 2:
                x = array[:, :, :1]

                # expand to what shape
                target = np.zeros((array.shape[0], array.shape[1], 3, 1))

                # do expand
                target[:x.shape[0], :x.shape[1], :1,0] = x

                array = target
            else:
                array =  array[:,:,:3]
        if len(array.shape) == 2:
            x = array[:, :]

            # expand to what shape
            target = np.zeros((array.shape[0], array.shape[1], 3, 1))

            # do expand
            target[:x.shape[0], :x.shape[1], 0, 0] = x

            array = target

        a = array
        a = np.interp(a, (a.min(), a.max()), (0, 256))
        array = a[:, :, :, :]
        array = array.swapaxes(2, 3)
        test_stack = array.astype('u1')
        shape_3d = test_stack.shape[0:3]
        rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])
        nana = test_stack.copy().view(rgb_dtype).reshape(shape_3d)
        img1 = nib.Nifti1Image(nana, np.eye(4))

        return img1



class ImageMetamorpher(MetamorphingOsloJobConsumer):

    def getDatabaseFunction(self):
        return update_image_on_display

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

