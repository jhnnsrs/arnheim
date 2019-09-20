import json

from channels.db import database_sync_to_async

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
def update_outputtransformation_or_create(request: Revamping, numpyarray, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"

    ## Get Correct
    vidfirst = "transformation_mask-{0}_revamper-{1}_node-{2}".format(str(request.mask_id),
                                                                        str(request.revamper_id),
                                                                        str(request.nodeid))
    transformations = Transformation.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(transformations.count) if transformations.count else 0)
    vid = vidfirst + vidsub
    transformation = transformations.last()  # TODO: CHeck if that makes sense

    if transformation is None or not settings.get("overwrite",False):
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
        transformation.vid = vid
        transformation.save()
    return transformation, method



