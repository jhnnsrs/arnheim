import json
from typing import Any, Dict, List, Tuple

import numpy as np
import xarray as xr
from django.db import models

from bioconverter.models import Representation
from bioconverter.serializers import RepresentationSerializer
from filterbank.models import Filtering
from filterbank.serializers import FilteringSerializer
from filterbank.utils import (get_filtering_or_error,
                              get_inputrepresentationbynode_or_error,
                              update_outputrepresentationbynode_or_create)
from larvik.consumers import DaskLarvikConsumer, DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob
from trontheim.consumers import OsloJobConsumer
import dask_image.ndfilters


class FilterConsumer(DaskSyncLarvikConsumer):

    def getRequest(self, data) -> LarvikJob:
        return Filtering.objects.get(pk=data["id"])

    def getSerializers(self):
        return {"Filtering": FilteringSerializer,
                "Representation": RepresentationSerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        raise NotImplementedError

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:
        raise NotImplementedError


@register_consumer("maxisp")
class MaxISP(FilterConsumer):

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:
        
        self.progress("Building Graph")
        rep: Representation = request.representation

        array: xr.DataArray = rep.array
        new = array.max(axis=3, keep_attrs=True)
        repout, graph = Representation.distributed.from_xarray_and_request(new, request, name=f"Max ISP of {rep.name}")
        
        self.progress("Evaluating Graph")
        graph.compute()

        return [(repout, "create")]


@register_consumer("slicedmaxisp")
class SlicedMaxISP(DaskSyncLarvikConsumer):

    def getRequest(self, data) -> LarvikJob:
        return Filtering.objects.get(pk=data["id"])

    def getSerializers(self):
        return {"Filtering": FilteringSerializer,
                "Representation": RepresentationSerializer}

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:

        array: xr.DataArray = request.representation.array
        print(array.z.size)

        lowerBound: int = int(settings.get("lowerBound",-1))
        upperBound: int = int(settings.get("upperBound",-1))



        array = array
        if len(array.shape) == 5:
            array = np.nanmax(array[:,:,:3,lowerBound:upperBound,0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:,:,:3,lowerBound:upperBound], axis=3)
        if len(array.shape) == 3:
            array = array[:,:,:3]
        if len(array.shape) == 2:
            array = array[:,:]

        self.progress("Saving File")
        rep, graph = Representation.distributed.from_xarray_and_request(array, request, name=f"Sliced MaxISP of {request.representation.name} at {request.nodeid}")
        self.progress("Computing Graph")
        graph.compute()

        return [(rep, "create")]

@register_consumer("prewitt")
class PrewittFilter(FilterConsumer):
    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:
        rep = request.representation

        channel = settings.get("channel", rep.array.channel[0])
        if "time" in rep.array.dims:
            it = rep.array.sel(time=0).sel(channel=channel)

        prewittfiltered = dask_image.ndfilters.prewitt(it.data)
        lala = xr.DataArray(prewittfiltered, coords=it.coords, name="data", attrs=it.attrs)

        rep, graph = Representation.distributed.from_xarray_and_request(lala, request, name=f"Max ISP of {rep.name}")
        graph.compute()
        return [(rep, "create")]


class Mapping(FilterConsumer):
    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:

        numpyarray = request.representation.loadArray()
        filtersettings = settings
        print(filtersettings)
        # Screens cant resolve more than three colors
        if len(numpyarray.shape) == 5:
            xdim = numpyarray.shape[0]
            ydim = numpyarray.shape[1]
            tdim = numpyarray.shape[3]
            zdim = numpyarray.shape[4]
            channels = numpyarray.shape[2]

            mappedfile = np.zeros((xdim, ydim, 3, tdim, zdim))
            mapping = filtersettings["mapping"]["channels"]
            # First Parameter will be the channels according to the file layout that need to be mapped
            map = [mapping["r"], mapping["g"], mapping["b"]]

            if len(map) < channels:
                print("Less then 3 Channels, skip last part of Map")
                map = map[:channels]

            # Case of More Channels than in Map is automatically handled

            for index, mappedchanneldict in enumerate(map):
                # Iterate over chosen channels

                mappedchannels = [ item["channel"] for item in mappedchanneldict]
                if len(mappedchannels) > 1:
                    channelsfromfile = np.nanmax(numpyarray.take(mappedchannels, axis=2), axis=2)  # maxisp of taken channels
                elif len(mappedchannels) == 1:
                    channelsfromfile = numpyarray[:, :, mappedchannels[0], :, :]
                else:
                    channelsfromfile = np.zeros((xdim, ydim, tdim, zdim))

                # channelsfromfile.append() #as we are casting a maxisp projection this is not really important
                # channelsfromfile = np.array(channelsfromfile)

                # maxispofchannelsfromfile = np.nanmax(channelsfromfile, axis=2)
                mappedfile[:, :, index, :, :] = channelsfromfile

        if len(numpyarray.shape) == 4:
            xdim = numpyarray.shape[0]
            ydim = numpyarray.shape[1]
            tdim = numpyarray.shape[3]
            channels = numpyarray.shape[2]

            mappedfile = np.zeros((xdim, ydim, 3, tdim))
            mapping = filtersettings["mapping"]["channels"]
            # First Parameter will be the channels according to the file layout that need to be mapped
            map = [mapping["r"], mapping["g"], mapping["b"]]

            if len(map) < channels:
                print("Less then 3 Channels, skip last part of Map")
                map = map[:channels]

            # Case of More Channels than in Map is automatically handled

            for index, mappedchanneldict in enumerate(map):
                # Iterate over chosen channels

                mappedchannels = [item["channel"] for item in mappedchanneldict]
                if len(mappedchannels) > 1:
                    channelsfromfile = np.nanmax(numpyarray.take(mappedchannels, axis=2),
                                                 axis=2)  # maxisp of taken channels
                elif len(mappedchannels) == 1:
                    channelsfromfile = numpyarray[:, :, mappedchannels[0], :]
                else:
                    channelsfromfile = np.zeros((xdim, ydim, tdim))

                # channelsfromfile.append() #as we are casting a maxisp projection this is not really important
                # channelsfromfile = np.array(channelsfromfile)

                # maxispofchannelsfromfile = np.nanmax(channelsfromfile, axis=2)
                mappedfile[:, :, index, :] = channelsfromfile

        if len(numpyarray.shape) == 3:
            xdim = numpyarray.shape[0]
            ydim = numpyarray.shape[1]
            channels = numpyarray.shape[2]

            mappedfile = np.zeros((xdim, ydim, 3))
            mapping = filtersettings["mapping"]["channels"]
            # First Parameter will be the channels according to the file layout that need to be mapped
            map = [mapping["r"], mapping["g"], mapping["b"]]

            if len(map) < channels:
                print("Less then 3 Channels, skip last part of Map")
                map = map[:channels]

            # Case of More Channels than in Map is automatically handled

            for index, mappedchanneldict in enumerate(map):
                # Iterate over chosen channels

                mappedchannels = [item["channel"] for item in mappedchanneldict]
                if len(mappedchannels) > 1:
                    channelsfromfile = np.nanmax(numpyarray.take(mappedchannels, axis=2),
                                                 axis=2)  # maxisp of taken channels
                elif len(mappedchannels) == 1:
                    channelsfromfile = numpyarray[:, :, mappedchannels[0]]
                else:
                    channelsfromfile = np.zeros((xdim, ydim))

                # channelsfromfile.append() #as we are casting a maxisp projection this is not really important
                # channelsfromfile = np.array(channelsfromfile)

                # maxispofchannelsfromfile = np.nanmax(channelsfromfile, axis=2)
                mappedfile[:, :, index] = channelsfromfile

        else:
            mappedfile = numpyarray

        print("Returned colormap shape {0}".format(str(mappedfile.shape)))

        rep, graph = Representation.distributed.from_array_and_request(mappedfile, request)
        graph.compute()
        return [(rep, "create")]
