import os
from typing import Dict, List, Tuple

import os
from typing import Dict, List, Tuple

import nibabel as nib
import numpy as np
import dask.array as da
from django.db import models
from rest_framework import serializers

from bioconverter.models import Representation
from larvik.consumers import LarvikError, DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from mandal.settings import NIFTI_ROOT, MEDIA_ROOT
from metamorphers.models import Metamorphing, Exhibit, Display, Metamorpher
from metamorphers.serializers import DisplaySerializer, ExhibitSerializer, MetamorphingSerializer
from metamorphers.utils import get_metamorphing_or_error, get_inputrepresentation_or_error
from trontheim.consumers import OsloJobConsumer


@register_consumer("exhibit", model=Metamorpher, )
class ExhibitMetamorpher(DaskSyncLarvikConsumer):
    type="metamorpher"
    name = "ExhibitMetamorpher"
    path = "ExhibitMetamorpher"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Exhibit]

    def getDefaultSettings(self, request: models.Model) -> str:
        return {"hallo": True}

    def getRequest(self, data):
        return Metamorphing.objects.get(pk=data["id"])

    def getSerializers(self):
        return {"Metamorphing": MetamorphingSerializer, "Exhibit": ExhibitSerializer}

    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:

        array = request.representation.array
        self.progress(f"Trying to Metamorph Array of Shape {array.shape}")

        print(array.dtype)
        if "t" in array.dims:
            array = array.sel(t=0)

        if "z" not in array.dims:
            raise LarvikError("This is not a Z-Stack")

        array.helpers.addChannel(tosize=3)  # Making sure we have enough

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
    type="metamorpher"
    name = "Image Metamorpher"
    path = "ImageMetamorpher"
    settings = {"reload": True,
                "overwrite": False}
    inputs = [Representation]
    outputs = [Display]

    def getRequest(self, data) -> LarvikJob:
        return Metamorphing.objects.get(pk=data["id"])

    def getSerializers(self):
        return {"Metamorphing": MetamorphingSerializer, "Display": DisplaySerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:

        array = request.representation.array

        if "z" in array.dims:
            array = array.max(dim="z")
        if "t" in array.dims:
            array = array.sel(t=0)

        print(array)
        if "c" in array.dims:
            if array.c.size >= 3:
                array = array.sel(c=[0,1,2]).data
            elif array.c.size == 2:
                array = da.concatenate([array.sel(c=[0,1]).data,da.zeros((array.x.size, array.y.size, 1))], axis=2)
            elif array.c.size == 1:
                raise NotImplementedError("We need to figure Matplotlib conversion for single-Channel Images")
        else:
            raise NotImplementedError("We need to figure Matplotlib conversion for single-Channel Images")


        self.progress("Rescaling")
        min, max = array.min(), array.max()
        print(array)
        array = np.interp(array.compute(), (min, max), (0, 255))
        array = array.astype(np.uint8)

        display = Display.objects.from_xarray_and_request(array, request)
        return [(display, "create")]
