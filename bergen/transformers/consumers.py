import json
from typing import Dict, Any, Callable, Awaitable, List, Tuple
import xarray as xr
import numpy as np
import dask.array as da
from django.db import models
from rest_framework import serializers

from drawing.models import LineROI
from elements.models import Representation, Transformation, ROI
from larvik.consumers import LarvikError, ModelFuncAsyncLarvikConsumer, DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from larvik.utils import update_status_on_larvikjob
from transformers.logic.linerectifier_logic import translateImageFromLine
from transformers.models import Transforming, Transformer
from transformers.serializers import TransformationSerializer, TransformingSerializer
from transformers.utils import get_transforming_or_error, outputtransformation_update_or_create
import larvik.extenders

# import the logging library
@register_consumer("linerect", model= Transformer)
class LineRectifierTransformer(DaskSyncLarvikConsumer):
    requestClass = Transforming
    type = "transformer"
    name = "Line Rectifier"
    path = "LineRectifier"
    settings = {"reload": True}
    inputs = [Representation, LineROI]
    outputs = [Transformation]


    def getSerializers(self):
        return {
            "Transforming": TransformingSerializer,
            "Transformation": TransformationSerializer,
        }

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"overwrite": True}

    def parse(self, request: Transforming, settings: dict) -> List[Tuple[str, Any]]:
        array = request.representation.array
        roi = request.roi


        physy = float(array.biometa.scan["PhysicalSizeY"])
        physx = float(array.biometa.scan["PhysicalSizeX"])


        self.progress("Getting Vectors")
        vectors = json.loads(roi.vectors)
        vertices = [[key["x"], key["y"]] for key in vectors]

        self.logger.info("Array has max of {0}".format(array.max()))

        self.progress("Conversing to Float64 for OpenCV")


        self.progress("Converting array")
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(settings.get("scale", 10)))

        self.progress("It actually Worked")
        outarray = xr.DataArray(da.array(image), dims=["x","y","c"])
        if physx != physy:
            self.progress("The Transformation is anisotropic. Discarding Physical Dimenions")
        else:
            outarray = xr.DataArray(outarray, coords = {"physx": outarray.x * physx,
                                                        "physy": outarray.y * physy,
                                                        "channels": array.channels,
                                                        "c": outarray.c,
                                                        "y": outarray.y,
                                                        "x": outarray.x})

        transformation, delayed = Transformation.delayed.from_xarray(outarray,
                                                            name="Line Rectification",
                                                            roi= request.roi,
                                                            transformer= request.transformer,
                                                            nodeid= request.nodeid,
                                                            creator = request.creator,
                                                            representation = request.representation
                                                            )

        delayed.compute()
        return [(transformation,"create")]




@register_consumer("sliceline", model= Transformer)
class SliceLineTransformer(ModelFuncAsyncLarvikConsumer):
    requestClass = Transforming
    type = "transformer"
    name = "Slice Line Rectifier"
    path = "SliceLineRectifier"
    settings = {"reload": True}
    inputs = [Representation, ROI, "Slice"]
    outputs = [Transformation]

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_transforming_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:

        return {"array": outputtransformation_update_or_create}

    def getSerializerDict(self) -> Dict[str, Any]:

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

        await self.progress("Getting array from file system")

        array = rep.array
        if "z" in array.dims:
            array = array.sel(z = slice(lowerBound,upperBound)).max(dim= "z")
        if "t" in array.dims:
            array = array.sel(t=0)
        if "c" in array.dims:
            array = array.sel(c=[0,1,2]) # Todo Probably not necessary

        self.logger.info("Collection Array of Shape {0} ".format(array.shape))
        self.logger.info("With Vertices like {0}".format(vertices))
        self.logger.info("Scale: {0}".format(scale))

        await self.progress("Selecting")
        self.logger.info("Maxed array of shape {0}".format(array.shape))
        array = np.float64(array)

        await self.progress("Transforming")
        image, boxwidths, pixelwidths, boxes = translateImageFromLine(array, vertices, int(scale))

        array = xr.DataArray(image, dims=["x","y","c"])
        return { "array" : array }
