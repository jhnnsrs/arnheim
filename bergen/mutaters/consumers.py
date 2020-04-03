from typing import Dict, List, Tuple

import numpy as np
from django.db import models

import dask.array as da
from elements.models import Transformation
from larvik.consumers import DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from mutaters.models import Mutater, Reflection, Mutating
from mutaters.serializers import MutatingSerializer, ReflectionSerializer


@register_consumer("imagemutater", model= Mutater)
class ImageMutator(DaskSyncLarvikConsumer):
    requestClass = Mutating
    name = "Image Mutater"
    path = "ImageMutater"
    type = "mutater"
    settings = {"reload": True}
    inputs = [Transformation]
    outputs = [Reflection]

    def getSerializers(self):
        return {"Mutating": MutatingSerializer, "Reflection": ReflectionSerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Mutating, settings: dict) -> List[Tuple[models.Model, str]]:

        rescale = True
        array = request.transformation.array

        if "z" in array.dims:
            array = array.max(dim="z")
        if "t" in array.dims:
            array = array.sel(t=0)

        if "c" in array.dims:
            # Check if we have to convert to monoimage
            if array.c.size == 1:
                array = array.sel(c=0)

                if rescale == True:
                    self.progress("Rescaling")
                    min, max = array.min(), array.max()
                    image = np.interp(array, (min, max), (0, 255)).astype(np.uint8)
                else:
                    image = (array * 255).astype(np.uint8)

                from matplotlib import cm
                mapped = cm.viridis(image)

                finalarray = (mapped * 255).astype(np.uint8)

            else:
                if array.c.size >= 3:
                    array = array.sel(c=[0, 1, 2]).data
                elif array.c.size == 2:
                    # Two Channel Image will be displayed with a Dark Channel
                    array = da.concatenate([array.sel(c=[0, 1]).data, da.zeros((array.x.size, array.y.size, 1))],
                                           axis=2)

                if rescale == True:
                    self.progress("Rescaling")
                    min, max = array.min(), array.max()
                    image = np.interp(array.compute(), (min, max), (0, 255)).astype(np.uint8)
                else:
                    image = (array * 255).astype(np.uint8)

                finalarray = image

        else:
            raise NotImplementedError("Image Does not provide the channel Argument")

        reflection = Reflection.objects.from_xarray_and_request(finalarray, request)
        return [(reflection, "create")]


