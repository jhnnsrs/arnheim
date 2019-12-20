from channels.db import database_sync_to_async
from evaluators.models import Evaluating, Data, VolumeData, ClusterData, LengthData
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_evaluating_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    evaluating = Evaluating.objects.get(pk=request["id"])
    if evaluating is None:
        raise ClientError("Evalutating {0} does not exist".format(str(request["id"])))
    return evaluating


@database_sync_to_async
def lengthdata_update_or_create(putdata, request: Evaluating, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "data_roi-{0}_transformation-{1}_evaluator-{2}_node-{3}".format(str(request.roi_id),str(request.transformation_id),str(request.evaluator_id),str(request.nodeid))
    datas = LengthData.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(datas.count()) if datas.count() else 0)
    vid = vidfirst + vidsub
    data: LengthData = datas.last()

    if data is None or not settings.get("overwrite", False):
        method = "create"
        # TODO make creation of outputvid
        logger.info("Creating New VolumeData with VID "+vid)
        data = LengthData.objects.create(
            name=request.evaluator.name + " of " + request.transformation.name + " of " + str(request.roi),
            creator=request.creator,
            vid=vid,
            evaluating=request,
            nodeid=request.nodeid,
            sample=request.sample,
            experiment=request.experiment,
            transformation=request.transformation,
            roi=request.roi,
            biometa=request.sample.meta,
            pixellength=putdata["length"],
            distancetostart=putdata["distancetostart"],
            distancetoend=putdata["distancetoend"],
            physicallength=putdata["physicallength"],
            physicaldistancetostart=putdata["physicaldistancetostart"],
            physicaldistancetoend=putdata["physicaldistancetoend"],
        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.pixellength = putdata["length"]
        data.distancetostart = putdata["distancetostart"]
        data.distancetoend = putdata["distancetoend"]
        data.physicallength = putdata["physicallength"]
        data.physicaldistancetostart = putdata["physicaldistancetostart"]
        data.physicaldistancetoend = putdata["physicaldistancetoend"]

    return [(data, method)]

@database_sync_to_async
def update_lengthdata_or_create(request: Evaluating, putdata: dict, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "data_roi-{0}_transformation-{1}_evaluator-{2}_node-{3}".format(str(request.roi_id),str(request.transformation_id),str(request.evaluator_id),str(request.nodeid))
    datas = LengthData.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(datas.count()) if datas.count() else 0)
    vid = vidfirst + vidsub
    data: LengthData = datas.last()

    if data is None or not settings.get("overwrite", False):
        method = "create"
        # TODO make creation of outputvid
        logger.info("Creating New VolumeData with VID "+vid)
        data = LengthData.objects.create(
            name=request.evaluator.name + " of " + request.transformation.name + " of " + str(request.roi),
            creator=request.creator,
            vid=vid,
            evaluating=request,
            nodeid=request.nodeid,
            sample=request.sample,
            experiment=request.experiment,
            transformation=request.transformation,
            roi=request.roi,
            biometa=request.sample.meta,
            pixellength=putdata["length"],
            distancetostart=putdata["distancetostart"],
            distancetoend=putdata["distancetoend"],
            physicallength=putdata["physicallength"],
            physicaldistancetostart=putdata["physicaldistancetostart"],
            physicaldistancetoend=putdata["physicaldistancetoend"],
        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.pixellength = putdata["length"]
        data.distancetostart = putdata["distancetostart"]
        data.distancetoend = putdata["distancetoend"]
        data.physicallength = putdata["physicallength"]
        data.physicaldistancetostart = putdata["physicaldistancetostart"]
        data.physicaldistancetoend = putdata["physicaldistancetoend"]

    return (data, method)

@database_sync_to_async
def clusterdata_update_or_create(putdata, request: Evaluating, settings):
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
            nodeid=request.nodeid,
            sample=request.sample,
            experiment=request.experiment,
            transformation=request.transformation,
            roi=request.roi,
            biometa=request.sample.meta,
            clusternumber=putdata["clusternumber"],
            clusterarea=putdata["clusterarea"],
            clusterareapixels=putdata["clusterareapixels"],
        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.clusternumber = putdata["clusternumber"],
        data.clusterarea = putdata["clusterarea"],
        data.clusterareapixels = putdata["clusterareapixels"],

    return [(data, method)]




@database_sync_to_async
def update_clusterdata_or_create(request: Evaluating, putdata: dict, settings):
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
            nodeid=request.nodeid,
            sample=request.sample,
            experiment=request.experiment,
            transformation=request.transformation,
            roi=request.roi,
            biometa=request.sample.meta,
            clusternumber=putdata["clusternumber"],
            clusterarea=putdata["clusterarea"],
            clusterareapixels=putdata["clusterareapixels"],
        )
    elif data is not None:
        # TODO: update array of output
        method = "update"
        # TODO: set name of newly generated and timestamp
        data.clusternumber = putdata["clusternumber"],
        data.clusterarea = putdata["clusterarea"],
        data.clusterareapixels = putdata["clusterareapixels"],

    return (data, method)


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
