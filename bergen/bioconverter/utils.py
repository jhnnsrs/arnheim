import json

import xarray
from channels.db import database_sync_to_async
from django.db import models

from bioconverter.models import Conversing, BioSeries, Analyzing
from elements.models import Sample, Representation
from larvik.structures import LarvikStatus


@database_sync_to_async
def get_conversing_or_error(request: dict) -> Conversing:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Conversing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ConversionRequest {0} does not exist".format(str(request["id"])))
    return parsing


@database_sync_to_async
def update_status_on_conversing(parsing: Conversing, status: LarvikStatus):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing.statuscode = status.statuscode
    parsing.statusmessage = status.message
    parsing.save()
    return parsing


@database_sync_to_async
def get_sample_or_error(sample: Sample) -> Sample:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Sample.objects.get(pk=sample.id)
    if parsing is None:
        raise ClientError("Sample {0} does not exist".format(str(sample.id)))
    return parsing



@database_sync_to_async
def update_outputrepresentation_or_create2(request: Conversing, sample: Sample, xarray: xarray.DataArray, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """


    rep = Representation.objects.from_xarray(xarray, name="Initial Stack", creator=request.creator, type="initial", chain="initial",
                                       sample=sample, nodeid=request.nodeid)


    #TODO: CHeck if that makes sense
    ## TODO: This really needs to be set by the meta correctly
    return rep, "create"


@database_sync_to_async
def create_sample_or_override(request: Conversing,settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    ## if override it should create a new Sample
    bioseries = request.bioserie
    if bioseries.sample is None:
        print("THIS IS CALLED?")
        sample = Sample.objects.create(name=request.bioserie.name, creator=request.creator,
                              experiment=request.experiment, nodeid= request.nodeid)

        bioseries.sample = sample
        bioseries.save()
        return bioseries.sample, "create"
    else:
        return bioseries.sample, "update"



@database_sync_to_async
def update_sample_with_meta(sample: Sample, meta: dict,settings=None):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    if sample is None:
        raise ClientError(f"Sample {sample} does not exist")
    elif sample is not None:
        # TODO: update array of output
        sample.save()
        method = "update"
    return sample, method




@database_sync_to_async
def update_sample_with_meta2(sample: Sample, meta: dict,settings=None):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    if sample is None:
        raise ClientError(f"Sample {sample} does not exist")
    elif sample is not None:
        # TODO: update array of output
        scan = meta["scan"]
        channellist = json.dumps(meta["channels"])

        sample.save()
        method = "update"
    return sample, method


@database_sync_to_async
def get_inputmodel_or_error(model, pk) -> models.Model:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    print(pk)
    print(model)
    inputmodel = model.objects.get(pk=pk)
    if inputmodel is None:
        raise ClientError("Inputmodel {0} does not exist".format(str(pk)))
    return inputmodel


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code




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





