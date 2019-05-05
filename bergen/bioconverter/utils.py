import io
import json
import os

import nibabel as nib
import numpy as np
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from bioconverter.logic.structures import BioMetaStructure
from bioconverter.models import ConversionRequest, Conversing
from drawing.models import Sample, BioMeta
from filterbank.models import Parsing, Representation, AImage, Nifti
from multichat.settings import MEDIA_ROOT


@database_sync_to_async
def get_conversing_or_error(request: dict) -> Conversing:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Conversing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ConversionRequest {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def get_sample_or_error(sample: Sample) -> Sample:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Sample.objects.get(pk=sample.id)
    if parsing is None:
        raise ClientError("Sample {0} does not exist".format(str(sample.id)))
    return parsing



@database_sync_to_async
def update_outputrepresentation_or_create(request: Conversing, sample: Sample, numpyarray, meta):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    outputrep: Representation = Representation.objects.filter(sample=sample.id).filter(
        nodeid=request.nodeid).first()

    ## TODO: This really needs to be set by the meta correctly
    repmeta = { "channels" : {"x": "px", "y": "px", "c": meta.channellist, "z": "NOTSET", "t" : "sec"}}
    repmetajson = json.dumps(repmeta)
    if outputrep is None:
        method = "create"
        outputrep = Representation.objects.create(name="Initial Stack", creator=request.creator, nodeid=request.nodeid,
                                                  sample=sample, experiment=request.experiment,
                                                  numpy=numpyarray, shape=json.dumps(numpyarray.shape), meta=repmetajson)
    elif outputrep is not None:
        method = "update"
        outputrep.nparray.set_array(numpyarray)
        outputrep.shape = json.dumps(numpyarray.shape)
        outputrep.meta = repmetajson
        outputrep.save()
    return outputrep, method


@database_sync_to_async
def create_sample_or_override(request: Conversing):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    ## if override it should create a new Sample
    method = "error"
    sample: Sample = Sample.objects.filter(name=request.bioserie.name).first()
    if sample is None:
        method = "create"
        # TODO make creation of outputvid
        sample = Sample.objects.create(name=request.bioserie.name, creator=request.creator, location="null",
                                            experiment=request.experiment, nodeid=request.nodeid, bioseries=request.bioserie)
        return sample, method
    elif sample is not None:
        # TODO: update array of output
        if not request.override:
            method = "create"
            return Sample.objects.create(name=request.bioserie.name, creator=request.creator, location="null",
                                            experiment=request.experiment, nodeid=request.nodeid, bioseries=request.bioserie), method
        else:
            method = "update"
            return sample, method


@database_sync_to_async
def update_sample_with_meta(sampleid, meta: BioMetaStructure):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    sample = Sample.objects.get(pk=sampleid)
    if sample is None:
        raise ClientError("Sample {0} does not exist".format(str(sampleid)))
    elif sample is not None:
        # TODO: update array of output
        outputmeta = BioMeta.objects.create(json=meta.unparsed,
                                            channellist=json.dumps(meta.channellist),
                                            xresolution=meta.sizex,
                                            yresolution=meta.sizey,
                                            zresolution=meta.sizez,
                                            cresolution=meta.sizec,
                                            tresolution=meta.sizet,
                                            xphysical=meta.physicalsizex,
                                            yphysical=meta.physicalsizey,
                                            zphysical=meta.physicalsizex,  # TODO: MAASSSSIVEE BUG
                                            spacial_units=meta.physicalsizexunit,
                                            temporal_units=meta.physicalsizeyunit,  # TODO: MASSIVE BUG HERE)
                                            )

        outputmeta.save()
        sample.meta = outputmeta
        sample.save()
        method = "update"
    return sample, method


@database_sync_to_async
def get_inputmodel_or_error(model, pk) -> models.Model:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    print(pk)
    print(model)
    inputmodel = model.objects.get(pk=pk)
    if inputmodel is None:
        raise ClientError("Inputmodel {0} does not exist".format(str(pk)))
    return inputmodel


@database_sync_to_async
def update_image_on_outputrepresentation_or_error(request: ConversionRequest, original_image, path) -> Representation:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(
        vid=request.outputvid).first()
    if outputrep is None:
        # TODO make creation of outputvid
        raise ClientError("VID {0} does nots exist on Sample {1}".format(str(request.outputvid), request.sample))
    elif outputrep is not None:
        # TODO: update array of output
        img_io = io.BytesIO()
        original_image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        if outputrep.image is None:
            outputrep.image = AImage()
            outputrep.image.save()

        model_image = AImage.objects.create(image=thumb_file)

        outputrep.image.image = thumb_file
        outputrep.image.save()
        outputrep.save()
        print("YES")
    return outputrep


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
