import os
from typing import Dict, List, Tuple

import dask.array as da
import xarray as xr
import nibabel as nib
import numpy as np
from django.db import models

from elements.models import Representation
from larvik.consumers import LarvikError, DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from django.conf import settings
from metamorphers.models import Metamorphing, Exhibit, Display, Metamorpher
from metamorphers.serializers import DisplaySerializer, ExhibitSerializer, MetamorphingSerializer


NIFTI_ROOT = settings.NIFTI_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT

@register_consumer("exhibit", model=Metamorpher, )
class ExhibitMetamorpher(DaskSyncLarvikConsumer):
    requestClass = Metamorphing
    type="metamorpher"
    name = "ExhibitMetamorpher"
    path = "ExhibitMetamorpher"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Exhibit]

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def getSerializers(self):
        return {"Metamorphing": MetamorphingSerializer, "Exhibit": ExhibitSerializer}

    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:
        self.progress("Building Graph")
        array: xr.DataArray = request.representation.array

        raise LarvikError("NOT IMPLEMENTED YET")

        self.progress(f"Trying to Metamorph Array of Shape {array.shape}")

        print(array.dtype)
        if "t" in array.dims:
            array = array.sel(t=0)

        if "z" not in array.dims:
            raise LarvikError("This is not a Z-Stack")

        self.helpers.addChannel(tosize=3)  # Making sure we have enough

        self.progress(f"Scaling")

        # Rescaling to classic Array Size
        array = array * 255
        array.astype("uint8")

        self.progress(f"Swapping Axes")
        array = array.transpose("x", "y", "z", "channel")
        array.compute()
        shape_3d = array.shape[0:3]
        self.progress(f"New Shape is {shape_3d}")
        rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])

        array = np.ascontiguousarray(array, dtype='u1')
        self.progress("Continuing Array")
        array = array.view(rgb_dtype).reshape(shape_3d)
        nifti = nib.Nifti1Image(array, np.eye(4))

        niftipaths = "sample-{0}_representation-{1}_nodeid-{2}.nii.gz".format(request.sample.id,
                                                                              request.representation.id, request.nodeid)
        niftipath = os.path.join(NIFTI_ROOT, niftipaths)
        nib.save(nifti, niftipath)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT, "/nifti"), niftipaths)
        name = "Exhibit of" + request.representation.name

        exhibit = Exhibit.objects.create(representation=request.representation, name=name, creator=request.creator,
                                         nodeid=request.nodeid, shape=request.representation.shape,
                                         sample=request.sample, experiment=request.representation.experiment,
                                         niftipath=niftiwebpath)

        return [(exhibit, "create")]


@register_consumer("image", model=Metamorpher)
class ImageMetamorpher(DaskSyncLarvikConsumer):
    requestClass = Metamorphing
    type="metamorpher"
    name = "Image Metamorpher"
    path = "ImageMetamorpher"
    settings = {"reload": True,
                "overwrite": False}
    inputs = [Representation]
    outputs = [Display]


    def getSerializers(self):
        return {"Metamorphing": MetamorphingSerializer, "Display": DisplaySerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:

        rescale = True
        array = request.representation.array

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
                    array = array.sel(c=[0,1,2]).data
                elif array.c.size == 2:
                    # Two Channel Image will be displayed with a Dark Channel
                    array = da.concatenate([array.sel(c=[0,1]).data,da.zeros((array.x.size, array.y.size, 1))], axis=2)

                if rescale == True:
                    self.progress("Rescaling")
                    min, max = array.min(), array.max()
                    image = np.interp(array.compute(), (min, max), (0, 255)).astype(np.uint8)
                else:
                    image = (array * 255).astype(np.uint8)

                finalarray = image

        else:
            raise NotImplementedError("Image Does not provide the channel Argument")


        display = Display.objects.from_xarray_and_request(finalarray, request)
        return [(display, "create")]
