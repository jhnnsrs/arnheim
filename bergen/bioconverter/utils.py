import json

import xarray
from channels.db import database_sync_to_async
from django.db import models

from bioconverter.logic.structures import BioMetaStructure
from bioconverter.models import Conversing, Representation
from elements.models import Sample
from biouploader.models import BioMeta


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
def update_status_on_conversing(parsing: Conversing, status):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing.status = status
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
def update_outputrepresentation_or_create(request: Conversing, sample: Sample, numpyarray, meta: BioMetaStructure, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    overwrite = settings.get("overwrite", True)
    physicalX = 0.65
    physicalY = 0.65
    physicalZ = 0.65

    # Representation Counts
    lala = xarray.DataArray(numpyarray, dims=('x', 'y', 'channels', "z", "time"), coords={'channels': meta.channellist})
    lala = xarray.DataArray(numpyarray, dims=('x', 'y', 'channels', "z", "time"),
                            coords={"x": (lala.x * physicalX), 'y': (lala.y * physicalY), "z": (lala.z * physicalZ),
                                    'channels': meta.channellist})
    lala.attrs["Seriesname"] = meta.seriesname
    lala.attrs['X-PhysicalSize'] = meta.physicalsizex
    lala.attrs['X-PhysicalSize-Unit'] = meta.physicalsizexunit
    lala.attrs['Y-PhysicalSize'] = meta.physicalsizey
    lala.attrs['Y-PhysicalSize-Unit'] = meta.physicalsizeyunit
    lala.attrs['AcquisitionDate'] = meta.date

    rep = Representation.objects.from_xarray(lala, name="Initial Stack", creator=request.creator, overwrite=overwrite,
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
    method = "error"
    sample: Sample = Sample.objects.filter(name=request.bioserie.name).first()
    if sample is None:
        method = "create"
        # TODO make creation of outputvid
        sample = Sample.objects.create(name=request.bioserie.name, creator=request.creator, location="null",
                                       experiment=request.experiment, nodeid=request.nodeid, bioseries=request.bioserie)
        return sample, method
    elif sample is not None:
        # TODO: update array of output
        if not settings.get("overwrite", False):
            method = "create"
            return Sample.objects.create(name=request.bioserie.name, creator=request.creator, location="null",
                                         experiment=request.experiment, nodeid=request.nodeid,
                                         bioseries=request.bioserie), method
        else:
            method = "update"
            return sample, method


@database_sync_to_async
def update_sample_with_meta(sampleid, meta: BioMetaStructure,settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    sample = Sample.objects.get(pk=sampleid)
    if sample is None:
        raise ClientError("Sample {0} does not exist".format(str(sampleid)))
    elif sample is not None:
        # TODO: update array of output
        outputmeta = BioMeta.objects.create(channellist=json.dumps(meta.channellist),
                                            xresolution=meta.sizex,
                                            yresolution=meta.sizey,
                                            zresolution=meta.sizez,
                                            cresolution=meta.sizec,
                                            tresolution=meta.sizet,
                                            xphysical=meta.physicalsizex,
                                            yphysical=meta.physicalsizey,
                                            zphysical=meta.physicalsizex,  # TODO: MAASSSSIVEE BUG
                                            spacial_units=meta.physicalsizexunit,
                                            temporal_units=meta.physicalsizeyunit,  # TODO: MASSIVE BUG HERE)
                                            )

        outputmeta.save()
        sample.meta = outputmeta
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
