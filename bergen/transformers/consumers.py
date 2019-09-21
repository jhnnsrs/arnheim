import json

import numpy as np

from bioconverter.models import Representation
from drawing.models import ROI
from transformers.logic.linerectifier_logic import translateImageFromLine
from transformers.models import Transforming
from transformers.serializers import TransformationSerializer
from transformers.utils import get_transforming_or_error, update_outputtransformation_or_create
from trontheim.consumers import OsloJobConsumer
# import the logging library

class TransformerConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Transforming = await get_transforming_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.transformer.defaultsettings)

        rep: Representation = request.representation
        roi: ROI = request.roi

        parsedarray = await self.parse(settings,rep,roi)


        transformation, method = await update_outputtransformation_or_create(request, settings, parsedarray)

        await self.modelCreated(transformation, TransformationSerializer, method)

    async def parse(self, settings: dict,rep: Representation, roi: ROI) -> np.array:
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


class LineRectifierTransformer(TransformerConsumer):


    async def parse(self, settings: dict, rep: Representation, roi: ROI) -> np.array:

        array = rep.numpy.get_array()
        vectors = json.loads(roi.vectors)

        vertices = [[key["x"],key["y"]] for key in vectors]

        print(array.max())
        array = np.float64(array)
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(settings["scale"]))


        return image



class SliceLineTransformer(TransformerConsumer):


    async def parse(self, settings: dict, rep: Representation, roi: ROI) -> np.array:

        shape = json.loads(rep.shape)
        z_size = shape[3]


        vectors = json.loads(roi.vectors)

        vertices = [[key["x"],key["y"]] for key in vectors]

        scale = settings["scale"]  if settings["scale"] else 10
        # We Have to Slice the Array first in order to make the transformation work
        lowerBound1: int = settings["lower"]  if settings["lower"] else 0
        upperBound1: int = settings["upper"]  if settings["upper"] and settings["upper"] is not -1 else z_size -1

        if lowerBound1 > upperBound1:
            lowerBound = upperBound1
            upperBound = lowerBound1
        else:
            lowerBound = lowerBound1
            upperBound = upperBound1


        array = rep.numpy.get_z_bounded_array(lowerBound,upperBound)

        print("Collection Array of Shape ", array.shape)
        print("With Vertices like",vertices)
        print("Scale: ",scale)

        if len(array.shape) == 5:
            array = np.nanmax(array[:, :, :3, :, 0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:, :, :3, :], axis=3)
        if len(array.shape) == 3:
            array = array[:, :, :3]
        if len(array.shape) == 2:
            array = array[:, :]

        print("Final array",array.shape)
        array = np.float64(array)
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(scale))


        return image
