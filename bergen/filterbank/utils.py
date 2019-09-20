import json

import numpy as np
from channels.db import database_sync_to_async

from bioconverter.models import Representation
from filterbank.models import Filtering
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
def get_inputrepresentationbynode_or_error(request: Filtering):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = request.representation
    if inputrep.numpy is not None:
        array = inputrep.numpy.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON THE REPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("InputNode {0} does not exist on Sample {1}".format(str(request.representation), request.sample))
    return inputrep, array



@database_sync_to_async
def update_outputrepresentationbynode_or_create(request: Filtering, numpyarray, inputrep: Representation , settings, meta):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    # Representation Counts
    vidfirst = "representation_representation-{0}_filter-{1}_node-{2}".format(str(inputrep.pk), str(request.filter_id), str(request.nodeid))
    representations = Representation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(representations.count()) if representations.count() else 0)
    vid = vidfirst + vidsub
    outputrep = representations.last()
    print(settings)
    if outputrep is None or settings["overwrite"] is False:
        method = "create"
        logger.info("Creating Representation with VID "+str(vid))
        #TODO make creation of outputvid
        outputrep = Representation.objects.create(name=request.filter.name + " of " + inputrep.name,
                                                  creator=request.creator,
                                                  nodeid=request.nodeid,
                                                  vid=vid,
                                                  sample=request.sample,
                                                  experiment=request.experiment,
                                                  nparray=numpyarray,
                                                  inputrep= inputrep,
                                                  meta= json.dumps(meta),
                                                  shape=json.dumps(numpyarray.shape)
                                                  )
    elif outputrep is not None:
        #TODO: update array of output
        method = "update"
        #TODO: set name of newly generated and timestamp
        outputrep.numpy.set_array(numpyarray)
        outputrep.shape = json.dumps(numpyarray.shape)
        outputrep.meta = json.dumps(meta)
        outputrep.save()
    return outputrep, method


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code