import json

import numpy as np

from drawing.models import ROI
from filterbank.models import Representation
from transformers.linerectifier_logic import translateImageFromLine
from transformers.models import Transforming
from transformers.serializers import TransformationSerializer
from transformers.utils import get_transforming_or_error, get_inputrepresentation_or_error, \
    update_outputtransformation_or_create
from trontheim.consumers import OsloJobConsumer


class TransformerConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Transforming = await get_transforming_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.transformer.defaultsettings)

        rep: Representation = request.representation
        roi: ROI = request.roi

        parsedarray = await self.parse(settings,rep,roi)

        vid = "transformation_roi-{0}_transformer-{1}".format(str(request.roi_id),str(request.transformer_id))
        transformation, method = await update_outputtransformation_or_create(request, parsedarray, vid)

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

        array = rep.nparray.get_array()
        vectors = json.loads(roi.vectors)

        vertices = [[key["x"],key["y"]] for key in vectors]

        print(array.max())

        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(settings["scale"]))

        from PIL import Image


        return image