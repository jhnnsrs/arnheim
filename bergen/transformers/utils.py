import json
import logging

from channels.db import database_sync_to_async

from transformers.models import Transforming
from elements.models import Transformation

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
def outputtransformation_update_or_create(numpyarray, request: Transforming, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "transformation_roi-{0}_transformer-{1}_node-{2}".format(str(request.roi_id), str(request.transformer_id), str(request.nodeid))

    transformations = Transformation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(transformations.count()) if transformations.count() else 0)
    vid = vidfirst + vidsub
    transformation = transformations.last() #TODO: CHeck if that makes sense
    if transformation is None or not settings["overwrite"]:
        method = "create"
        logger.info("Creating Transformation with VID: " + vid)
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
        logger.info("Updating Transformation with VID: " + vid)
        #TODO: set name of newly generated and timestamp
        transformation.numpy.set_array(numpyarray)
        transformation.shape = json.dumps(numpyarray.shape)
        transformation.nodeid = request.nodeid
        transformation.save()
    return [(transformation, method)]


@database_sync_to_async
def update_outputtransformation_or_create(request: Transforming, settings, numpyarray):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "transformation_roi-{0}_transformer-{1}_node-{2}".format(str(request.roi_id), str(request.transformer_id), str(request.nodeid))

    transformations = Transformation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(transformations.count()) if transformations.count() else 0)
    vid = vidfirst + vidsub
    transformation = transformations.last() #TODO: CHeck if that makes sense
    if transformation is None or not settings["overwrite"]:
        method = "create"
        logger.info("Creating Transformation with VID: " + vid)
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
        logger.info("Updating Transformation with VID: " + vid)
        #TODO: set name of newly generated and timestamp
        transformation.numpy.set_array(numpyarray)
        transformation.shape = json.dumps(numpyarray.shape)
        transformation.nodeid = request.nodeid
        transformation.save()
    return transformation, method



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code