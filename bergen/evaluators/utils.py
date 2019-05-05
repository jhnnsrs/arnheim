from channels.db import database_sync_to_async
from evaluators.models import Evaluating, Data, VolumeData


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
def update_data_or_create(request: Evaluating, putdata: VolumeData, vid):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    data: VolumeData = VolumeData.objects.filter(sample=request.sample).filter(vid=vid).first()
    if data is None:
        method = "create"
        # TODO make creation of outputvid
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


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
