from channels.db import database_sync_to_async
from evaluators.models import Evaluating, Data, VolumeData, ClusterData
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_evaluating_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    evaluating = Evaluating.objects.get(pk=request["id"])
    if evaluating is None:
        raise ClientError("Evalutating {0} does not exist".format(str(request["id"])))
    return evaluating


@database_sync_to_async
def update_volumedata_or_create(request: Evaluating, putdata: VolumeData, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "data_roi-{0}_transformation-{1}_evaluator-{2}_node-{3}".format(str(request.roi_id),str(request.transformation_id),str(request.evaluator_id),str(request.nodeid))
    datas = VolumeData.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(datas.count()) if datas.count() else 0)
    vid = vidfirst + vidsub
    data: VolumeData = datas.last()

    if data is None or not settings["override"]:
        method = "create"
        # TODO make creation of outputvid
        logger.info("Creating New VolumeData with VID "+vid)
        data = VolumeData.objects.create(
            name=request.evaluator.name + " of " + request.transformation.name + " of " + str(request.roi),
            creator=request.creator,
            vid=vid,
            nodeid=putdata.nodeid,
            sample=putdata.sample,
            experiment=putdata.experiment,
            transformation=putdata.transformation,
            roi=putdata.roi,
            b4channel=putdata.b4channel,
            vectorlength=putdata.vectorlength,
            pixellength=putdata.pixellength,
            aisstart=putdata.aisstart,
            aisend=putdata.aisend,
            userdefinedstart=putdata.userdefinedstart,
            userdefinedend=putdata.userdefinedend,
            threshold=putdata.threshold,
            physicallength=putdata.physicallength,
            tags=putdata.tags,
            diameter=3,
            meta=putdata.meta,
            intensitycurves=putdata.intensitycurves,

        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.vectorlength = putdata.vectorlength,

    return data, method

@database_sync_to_async
def update_clusterdata_or_create(request: Evaluating, putdata: ClusterData, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "data_roi-{0}_transformation-{1}_evaluator-{2}_node-{3}".format(str(request.roi_id),
                                                                               str(request.transformation_id),
                                                                               str(request.evaluator_id),
                                                                               str(request.nodeid))
    datas = ClusterData.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(datas.count()) if datas.count() else 0)
    vid = vidfirst + vidsub
    data: ClusterData = datas.last()
    if data is None or not settings.get("overwrite", False):
        method = "create"
        # TODO make creation of outputvid
        logger.info("Creating New ClusterData with VID " + vid)
        data = ClusterData.objects.create(
            name=request.evaluator.name + " of " + request.transformation.name + " of " + str(request.roi),
            creator=request.creator,
            vid=vid,
            nodeid=putdata.nodeid,
            sample=putdata.sample,
            experiment=putdata.experiment,
            transformation=putdata.transformation,
            roi=putdata.roi,
            tags=putdata.tags,
            meta=putdata.meta,
            clusternumber=putdata.clusternumber,
            clusterarea=putdata.clusterarea,
            clusterareapixels=putdata.clusterareapixels,
            spatialunit=putdata.spatialunit,
        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.clusternumber = putdata.clusternumber,

    return data, method


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
