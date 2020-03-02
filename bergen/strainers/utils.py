import json
import logging

from channels.db import database_sync_to_async

from strainers.models import Straining
from elements.models import Transformation

# Get an instance of a logger
logger = logging.getLogger(__name__)


@database_sync_to_async
def get_straining_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Straining.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Straining {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def outputtransformation_update_or_create(numpyarray, request: Straining, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "transformation_transformation-{0}_strainer-{1}_node-{2}".format(str(request.transformation_id), str(request.strainer_id), str(request.nodeid))

    transformations = Transformation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(transformations.count()) if transformations.count() else 0)
    vid = vidfirst + vidsub
    transformation = transformations.last() #TODO: CHeck if that makes sense
    if transformation is None or not settings.get("overwrite",False):
        method = "create"
        logger.info("Creating Transformation with VID: " + vid)
        #TODO make creation of outputvid
        transformation = Transformation.objects.create(name=request.strainer.name + " of " + request.transformation.name,
                                                       creator=request.creator,
                                                       vid=vid,
                                                       sample=request.sample,
                                                       experiment=request.experiment,
                                                       nparray=numpyarray,
                                                       shape=json.dumps(numpyarray.shape),
                                                       inputtransformation=request.transformation,
                                                       representation=request.transformation.representation,
                                                       roi=request.transformation.roi,
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
def update_outputtransformation_or_create(request: Straining, settings, numpyarray):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "transformation_transformation-{0}_strainer-{1}_node-{2}".format(str(request.transformation_id), str(request.strainer_id), str(request.nodeid))

    transformations = Transformation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(transformations.count()) if transformations.count() else 0)
    vid = vidfirst + vidsub
    transformation = transformations.last() #TODO: CHeck if that makes sense
    if transformation is None or not settings.get("overwrite",False):
        method = "create"
        logger.info("Creating Transformation with VID: " + vid)
        #TODO make creation of outputvid
        transformation = Transformation.objects.create(name=request.strainer.name + " of " + request.transformation.name,
                                                       creator=request.creator,
                                                       vid=vid,
                                                       sample=request.sample,
                                                       experiment=request.experiment,
                                                       nparray=numpyarray,
                                                       shape=json.dumps(numpyarray.shape),
                                                       inputtransformation=request.transformation,
                                                       representation=request.transformation.representation,
                                                       roi=request.transformation.roi,
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
    return (transformation, method)



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code