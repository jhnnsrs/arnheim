import io
import json

import numpy as np
from channels.db import database_sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile

from bioconverter.models import ConversionRequest
from filterbank.models import Parsing, Representation, AImage, Filtering


@database_sync_to_async
def get_parsingrequest_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Parsing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ParsingRequest {0} does not exist".format(str(request["id"])))
    return parsing


@database_sync_to_async
def get_filtering_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    filtering = Filtering.objects.get(pk=request["id"])
    if filtering is None:
        raise ClientError("Filtering {0} does not exist".format(str(request["id"])))
    return filtering


@database_sync_to_async
def get_inputrepresentationbyvid_or_error(request: Parsing):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.inputvid).first()
    if inputrep.nparray is not None:
        array = inputrep.nparray.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON THE REPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("Inputvid {0} does not exist on Sample {1}".format(str(request.inputvid), request.sample))
    return inputrep, array

@database_sync_to_async
def get_inputrepresentationbynode_or_error(request: Filtering):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = request.representation
    if inputrep.nparray is not None:
        array = inputrep.nparray.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON THE REPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("InputNode {0} does not exist on Sample {1}".format(str(request.representation), request.sample))
    return inputrep, array


@database_sync_to_async
def update_outputrepresentation_or_create(request: Parsing, numpyarray, inputrep):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        method = "create"
        #TODO make creation of outputvid
        outputrep = Representation.objects.create(name=request.filter.name + " of " + inputrep.name,creator=request.creator,vid=request.outputvid,sample=request.sample,experiment=request.experiment,numpy=numpyarray,shape=json.dumps(numpyarray.shape))
    elif outputrep is not None:
        #TODO: update array of output
        method = "update"
        #TODO: set name of newly generated and timestamp
        outputrep.nparray.set_array(numpyarray)
        outputrep.shape = json.dumps(numpyarray.shape)
        outputrep.save()
    return outputrep, method

@database_sync_to_async
def update_outputrepresentationbynode_or_create(request: Filtering, numpyarray, inputrep: Representation , settings, meta):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    outputrep: Representation = Representation.objects.filter(inputrep=request.representation).filter(nodeid=request.nodeid).first()
    print(settings)
    if outputrep is None or settings["overwrite"] is False:
        method = "create"
        #TODO make creation of outputvid
        outputrep = Representation.objects.create(name=request.filter.name + " of " + inputrep.name,
                                                  creator=request.creator,
                                                  nodeid=request.nodeid,
                                                  sample=request.sample,
                                                  experiment=request.experiment,
                                                  numpy=numpyarray,
                                                  inputrep= inputrep,
                                                  meta= json.dumps(meta),
                                                  shape=json.dumps(numpyarray.shape)
                                                  )
    elif outputrep is not None:
        #TODO: update array of output
        method = "update"
        #TODO: set name of newly generated and timestamp
        outputrep.nparray.set_array(numpyarray)
        outputrep.shape = json.dumps(numpyarray.shape)
        outputrep.meta = json.dumps(meta)
        outputrep.save()
    return outputrep, method

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