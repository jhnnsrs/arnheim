import io
import json

import numpy as np
from channels.db import database_sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile

from bioconverter.models import ConversionRequest
from filterbank.models import Parsing, Representation, AImage
from transformers.models import Transforming, Transformation


@database_sync_to_async
def get_transforming_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Transforming.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Transforming {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def get_masking_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Masking.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Masking {0} does not exist".format(str(request["id"])))
    return parsing


@database_sync_to_async
def get_inputrepresentation_or_error(request: Transforming):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = Representation.objects.get(pk=request.representation)
    if inputrep.nparray is not None:
        array = inputrep.nparray.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON THE REPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("Representation {0} does not exist".format(str(request.representation)))
    return inputrep, array


@database_sync_to_async
def update_outputtransformation_or_create(request: Transforming, numpyarray, vid):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    transformation: Transformation = Transformation.objects.filter(sample=request.sample).filter(vid=vid).first()
    if transformation is None:
        method = "create"
        #TODO make creation of outputvid
        transformation = Transformation.objects.create(name=request.transformer.name + " of " + request.representation.name + " of " + str(request.roi) ,
                                                       creator=request.creator,
                                                       vid=vid,
                                                       sample=request.sample,
                                                       experiment=request.experiment,
                                                       nparray=numpyarray,
                                                       shape=json.dumps(numpyarray.shape),
                                                       representation=request.representation,
                                                       roi=request.roi,
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




@database_sync_to_async
def update_image_onoutputrepresentation_or_error(request: Parsing, original_image, path):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does not exist on Sample {1}".format(str(request.outputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        original_image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        if outputrep.image is None:
            outputrep.image = AImage()
            outputrep.image.save()

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