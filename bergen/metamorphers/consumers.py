import json
import os
from typing import Dict, Any, Callable, Awaitable, List, Tuple

import nibabel as nib
import numpy as np
from django.db import models
from rest_framework import serializers

from filterbank.logic.addins import toimage
from larvik.consumers import LarvikConsumer, LarvikError, DaskLarvikConsumer, DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from larvik.utils import update_status_on_larvikjob
from mandal.settings import NIFTI_ROOT, MEDIA_ROOT
from metamorphers.models import Metamorphing, Exhibit, Display
from metamorphers.serializers import DisplaySerializer, ExhibitSerializer, MetamorphingSerializer
from metamorphers.utils import get_metamorphing_or_error, get_inputrepresentation_or_error, \
    update_display_or_create, exhibit_update_or_create
from trontheim.consumers import OsloJobConsumer


class MetamorphingOsloJobConsumer(OsloJobConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.request = None

    async def startJob(self, data):
        await self.register(data)
        print(data)
        request: Metamorphing = await get_metamorphing_or_error(data["data"])
        self.request = request
        settings: dict = await self.getsettings(request.settings, request.metamorpher.defaultsettings)

        inputrep, array = await get_inputrepresentation_or_error(request)

        file = await self.convert(array, settings)
        if not file: return

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



@register_consumer("nifti")
class NiftiMetamorpher(DaskSyncLarvikConsumer):

    def getDefaultSettings(self, request: models.Model) -> str:
        return {"hallo": True}

    def getRequest(self,data):
        return Metamorphing.objects.get(pk=data["id"])

    def getSerializers(self):
        return { "Metamorphing": MetamorphingSerializer, "Exhibit": ExhibitSerializer}


    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:

        array = request.representation.loadArray()
        self.progress(f"Trying to Metamorph Array of Shape {array.shape}")

        rescale = settings.get("rescale", False)
        if len(array.shape) != 5:
            raise LarvikError("Not the right shape for the job")

        print(array.dtype)
        array = array[:, :, :, :, 0]
        self.progress(f"Reducing Dimensions")
        array = array.compute()

        cmin = array.min()
        cmax = array.max()
        high = 255
        low = 0

        cscale = cmax - cmin
        if cscale < 0:
            raise LarvikError("`cmax` should be larger than `cmin`.")
        elif cscale == 0:
            cscale = 1

        scale = float(high - low) / cscale
        if rescale:
            self.progress(f"Interpolating from {cmin} to {cmax}")
            array = (array - cmin) * scale + low
            array = (array.clip(low, high) + 0.5).astype("uint8")
        else:
            array = array * 255

        array = array.astype("u1")
        self.progress(f"Swapping Axes")
        array = np.swapaxes(array,2,3)
        shape_3d = array.shape[0:3]
        self.progress(f"New Shape is {shape_3d}")
        rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])

        array = np.ascontiguousarray(array, dtype='u1')
        self.progress("Continuing Array")
        array = array.view(rgb_dtype).reshape(shape_3d)
        nifti = nib.Nifti1Image(array, np.eye(4))

        niftipaths = "sample-{0}_representation-{1}_nodeid-{2}.nii.gz".format(request.sample.id,request.representation.id, request.nodeid)
        niftipath = os.path.join(NIFTI_ROOT, niftipaths)
        nib.save(nifti, niftipath)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT, "/nifti"), niftipaths)
        name = "Exhibit of" + request.representation.name

        exhibit = Exhibit.objects.create(representation=request.representation, name=name, creator=request.creator,
                                         nodeid=request.nodeid, shape=request.representation.shape,
                                         sample=request.sample, experiment=request.representation.experiment,
                                         niftipath=niftiwebpath)

        return [(exhibit, "create")]



@register_consumer("image")
class ImageMetamorpher(DaskSyncLarvikConsumer):

    def getRequest(self, data) -> LarvikJob:
        return Metamorphing.objects.get(pk=data["id"])

    def getSerializers(self):
        return { "Metamorphing": MetamorphingSerializer, "Display": DisplaySerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo":True}

    def parse(self, request: Metamorphing, settings: dict) -> List[Tuple[models.Model, str]]:

        array = request.representation.loadArray()

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

        display = Display.objects.from_xarray_and_request(array, request)
        return [(display, "create")]




