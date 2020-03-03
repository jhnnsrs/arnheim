import json

import numpy as np
from rest_framework import serializers

from larvik.consumers import AsyncLarvikConsumer
from larvik.discover import register_consumer
from revamper.models import Revamping, Mask, Revamper
from revamper.utils import get_revamping_or_error, update_outputtransformation_or_create
from elements.models import Transformation
from transformers.serializers import TransformationSerializer


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
