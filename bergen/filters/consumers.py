import json
from typing import Any, Dict, List, Tuple

import dask_image.ndfilters
import dask.array as da
import numpy as np
import xarray as xr
from django.db import models

from bioconverter.models import Representation
from bioconverter.nodes import Channel
from bioconverter.serializers import RepresentationSerializer
from filters.models import Filter, Filtering
from filters.serializers import FilteringSerializer
from larvik.consumers import DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.models import LarvikJob


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


@register_consumer("maxisp",model= Filter)
class MaxISP(FilterConsumer):
    name = "Max ISP"
    path = "MaxISP"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Representation]

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



@register_consumer("slicedmaxisp",model= Filter)
class SlicedMaxISP(FilterConsumer):
    name = "Sliced Max ISP"
    path = "SlicedMaxISP"
    settings = {"reload": True}
    inputs = [Representation, "Slice"]
    outputs = [Representation]

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

@register_consumer("prewitt",model= Filter)
class PrewittFilter(FilterConsumer):
    name = "Prewitt"
    path = "Prewitt"
    settings = {"reload": True}
    inputs = [Representation, Channel]
    outputs = [Representation]

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:
        it = request.representation.array

        if "t" in it.dims:
            it = it.sel(t=0)
        if "c" in it.dims:
            meta = it.biometa.channels
            channel = settings.get("channel", 0)
            self.progress(f"Selecting Channels {meta['Name'][channel]}")
            it = it.sel(c=channel)

        prewittfiltered = dask_image.ndfilters.prewitt(it.data)

        outarray = xr.DataArray(prewittfiltered, dims=["x", "y"],
                             coords={"x": it.x, "y": it.y, "physx": it.physx, "physy": it.physy})

        rep, graph = Representation.distributed.from_xarray_and_request(outarray, request, name=f"Prewitt Filter of {request.representation.name}")
        graph.compute()
        return [(rep, "create")]


@register_consumer("mapping",model= Filter)
class Mapping(FilterConsumer):
    name = "Mapping"
    path = "Mapping"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Representation]

    def getDefaultSettings(self, request: models.Model) -> Dict:
        return {"hallo": True}

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:

        def merge(channels, el):
            items = el.sel(c=channels).channels.data.compute()
            if len(items) == 1:
                return items[0]
            name = ",".join([item["Name"] for item in items])

            merge = items[0]
            merge["Index"] = -1
            merge["Name"] = f"Merged Channel ({name})"
            return merge

        array = request.representation.array
        threed = array

        rchannel = threed.sel(c=[1, 0])
        gchannel = threed.sel(c=[1, 0])
        bchannel = threed.sel(c=[0])

        rmeta = merge([1, 0], threed)
        gmeta = merge([1, 0], threed)
        bmeta = merge([0], threed)

        channels = xr.DataArray(da.from_array([rmeta, gmeta, bmeta]), dims=["c"])

        r = rchannel.max(dim="c", keepdims=True)
        g = gchannel.max(dim="c", keepdims=True)
        b = bchannel.max(dim="c", keepdims=True)

        x = da.concatenate([r.data, g.data, b.data], axis=2)
        x = xr.DataArray(x, dims=threed.dims, coords={**threed.coords, "channels": channels, "c": range(3)})

        rep, graph = Representation.distributed.from_array_and_request(x, request, name=f"RGB Mapping of {request.representation.name}")
        graph.compute()
        return [(rep, "create")]
