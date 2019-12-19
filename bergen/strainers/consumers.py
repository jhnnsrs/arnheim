import json

import numpy as np

from bioconverter.models import Representation
from drawing.models import ROI
from strainers.models import Straining
from strainers.serializers import StrainingSerializer
from strainers.utils import get_straining_or_error, update_outputtransformation_or_create
from transformers.models import  Transformation
from transformers.serializers import TransformationSerializer
from trontheim.consumers import OsloJobConsumer
# import the logging library

class StrainerConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Straining = await get_straining_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.strainer.defaultsettings)

        transformation: Transformation = request.transformation

        parsedarray = await self.parse(settings,transformation)

        transformation, method = await update_outputtransformation_or_create(request, settings, parsedarray)

        await self.modelCreated(transformation, TransformationSerializer, method)

    async def parse(self, settings: dict,rep: Representation, roi: ROI) -> np.array:
        raise NotImplementedError

    async def raiseError(self, error):
        self.data["error"] = error
        await self.modelCreated(self.data, StrainingSerializer, "update")

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


class IntensityProfiler(StrainerConsumer):


    async def parse(self, settings: dict, transformation: Transformation) -> np.array:


        transformation_image = transformation.numpy.get_array()
        height = 0
        ndim = 2

        if len(transformation_image.shape) > 3 or len(transformation_image.shape) < 2:
            await self.raiseError("This is not a valid transformation. Shape exceeds the available dimensions")
            return
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
            print("Original Intensitycurve had shape of ",intensity.shape)
            selectedchannels = list(map(lambda item: item["value"], settings["channels"]))
            print("Selecting Channels ",selectedchannels)
            intensity = np.take(intensity, selectedchannels, axis=1)
            print("Intensitycurves now has shape of ",intensity.shape)

        return intensity

class Masker(StrainerConsumer):


    async def parse(self, settings: dict, transformation: Transformation) -> np.array:


        array = transformation.numpy.get_array()


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

        return restored
