import io
import json
import os

import nibabel as nib
import numpy as np
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from bioconverter.models import ConversionRequest
from filterbank.models import Parsing, Representation, AImage, Nifti
from metamorphers.models import Metamorphing
from multichat.settings import MEDIA_ROOT
from mutaters.models import Mutating, Reflection
from revamper.models import Revamping
from transformers.models import Transformation


@database_sync_to_async
def get_revamping_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Revamping.objects.get(pk=request["id"])
    if parsing is None:
        raise Exception("Mutating {0} does not exist".format(str(request["id"])))
    return parsing



@database_sync_to_async
def update_outputtransformation_or_create(request: Revamping, numpyarray, vid):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    transformation: Transformation = Transformation.objects.filter(sample=request.sample).filter(vid=vid).first()
    if transformation is None:
        method = "create"
        #TODO make creation of outputvid
        transformation = Transformation.objects.create(name=request.revamper.name + " of " + request.transformation.name ,
                                                       creator=request.creator,
                                                       vid=vid,
                                                       sample=request.sample,
                                                       experiment=request.transformation.experiment,
                                                       nparray=numpyarray,
                                                       shape=json.dumps(numpyarray.shape),
                                                       representation=request.transformation.representation,
                                                       roi=request.transformation.roi,
                                                       nodeid=request.nodeid)
    elif transformation is not None:
        #TODO: update array of output
        method = "update"
        #TODO: set name of newly generated and timestamp
        transformation.numpy.set_array(numpyarray)
        transformation.shape = json.dumps(numpyarray.shape)
        transformation.nodeid = request.nodeid
        transformation.save()
    return transformation, method



