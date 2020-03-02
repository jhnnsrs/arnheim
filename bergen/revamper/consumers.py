import json

import numpy as np
from rest_framework import serializers

from larvik.consumers import AsyncLarvikConsumer
from larvik.discover import register_consumer
from revamper.models import Revamping, Mask, Revamper
from revamper.utils import get_revamping_or_error, update_outputtransformation_or_create
from elements.models import Transformation
from transformers.serializers import TransformationSerializer
from trontheim.consumers import OsloJobConsumer


class RevampingOsloJob(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startconverting(self, data):
        await self.register(data)
        print(data)
        request: Revamping = await get_revamping_or_error(data["data"])
        self.request = request
        mask = request.mask
        settings: dict = await self.getsettings(request.settings, request.revamper.defaultsettings)

        array = request.transformation.numpy.get_array()

        newarray = await self.convert(array, mask, settings)

        func = self.getDatabaseFunction()
        model, method = await func(request, newarray, settings)

        await self.modelCreated(model, self.getSerializer(), method)

    async def convert(self, array: np.array, mask: Mask, settings: dict):
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




@register_consumer("masking", model= Revamper)
class MaskingRevamper(AsyncLarvikConsumer):
    name = "Masker"
    path = "Masker"
    settings = {"reload": True}
    inputs = [Transformation, Mask]
    outputs = [Transformation]

    def getDatabaseFunction(self):
        return update_outputtransformation_or_create

    def getSerializer(self):
        return TransformationSerializer

    async def convert(self, array: np.array, mask: Mask, conversionsettings: dict):
        # TODO: Maybe faktor this one out
        print(array.shape)
        vec = json.loads(mask.vectors)

        x, y = np.meshgrid(np.arange(array.shape[1]), np.arange(array.shape[0]))
        pix = np.vstack((x.flatten(), y.flatten())).T
        clustermask = np.zeros_like(array[:, :, 0])


        restored = clustermask
        for el in vec:
            restored.flat[el] = 1
        print(restored.shape)
        return restored
