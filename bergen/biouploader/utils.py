from channels.db import database_sync_to_async

from biouploader.models import Analyzing, BioSeries


@database_sync_to_async
def get_analyzing_or_error(request: dict) -> Analyzing:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Analyzing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Analyzing {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def get_analyzing_or_error(request: dict) -> Analyzing:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Analyzing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Analyzing {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def bioseries_create_or_update(series: [], request: Analyzing, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request.bioimage.locker_id)
    createBioseries = []
    for bio in series:
        method = "error"
        outputseries: BioSeries = BioSeries.objects.filter(bioimage=request.bioimage).filter(index=bio["index"]).first()
        if outputseries is None:
            method = "create"
            # TODO make creation of outputvid
            outputseries = BioSeries.objects.create(name=bio["name"],
                                                    creator=request.creator,
                                                    index=bio["index"],
                                                    isconverted=False,
                                                    bioimage=request.bioimage,
                                                    nodeid=request.nodeid,
                                                    locker=request.bioimage.locker)

        elif outputseries is not None:
            # TODO: update array of output
            method = "update"
            outputseries.name = bio["name"]
            outputseries.creator = request.creator
            outputseries.index = bio["index"]
            outputseries.nodeid = request.nodeid
            outputseries.locker = request.bioimage.locker
            outputseries.save()

        createBioseries.append((outputseries, method))

    return createBioseries



@database_sync_to_async
def update_bioseries_or_create(request: Analyzing, bio: BioSeries):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(bio.locker_id)
    method = "error"
    outputseries: BioSeries = BioSeries.objects.filter(bioimage=request.bioimage).filter(index=bio.index).first()
    if outputseries is None:
        method = "create"
        # TODO make creation of outputvid
        outputseries = BioSeries.objects.create(name=bio.name,
                                                creator=request.creator,
                                                index=bio.index,
                                                isconverted=False,
                                                bioimage=request.bioimage,
                                                nodeid=bio.nodeid,
                                                locker_id=bio.locker_id)

    elif outputseries is not None:
        # TODO: update array of output
        method = "update"
        outputseries.name = bio.name
        outputseries.creator = request.creator
        outputseries.index = bio.index
        outputseries.nodeid = bio.nodeid
        outputseries.locker_id = bio.locker_id
        outputseries.save()
    return outputseries, method





class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
