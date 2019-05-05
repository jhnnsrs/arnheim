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
from bioconverter.models import ConversionRequest
from biouploader.models import Analyzing, BioSeries
from drawing.models import Sample, BioMeta
from filterbank.models import Parsing, Representation, AImage, Nifti
from multichat.settings import MEDIA_ROOT


@database_sync_to_async
def get_analyzing_or_error(request: dict) -> ConversionRequest:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Analyzing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Analyzing {0} does not exist".format(str(request["id"])))
    return parsing


@database_sync_to_async
def update_bioseries_or_create(request: Analyzing, bio: BioSeries):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(bio.locker_id)
    method = "error"
    outputseries: BioSeries = BioSeries.objects.filter(bioimage=request.bioimage).filter(index=bio.index).first()
    if outputseries is None:
        method = "create"
        # TODO make creation of outputvid
        outputseries = BioSeries.objects.create(name=bio.name,
                                                creator=request.creator,
                                                index=bio.index,
                                                experiment= request.bioimage.experiment,
                                                isconverted=False,
                                                bioimage=request.bioimage,
                                                nodeid=bio.nodeid,
                                                locker_id=bio.locker_id)

    elif outputseries is not None:
        # TODO: update array of output
        method = "update"
        outputseries.name = bio.name
        outputseries.creator = request.creator
        outputseries.experiment = request.bioimage.experiment
        outputseries.index = bio.index
        outputseries.nodeid = bio.nodeid
        outputseries.locker_id = bio.locker_id
        outputseries.save()
    return outputseries, method





class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
