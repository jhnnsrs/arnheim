import json
from typing import Any, Dict, List, Tuple

import dask_image.ndfilters
import dask.array as da
import numpy as np
import xarray as xr
from django.db import models

from bioconverter.models import Representation
from bioconverter.serializers import RepresentationSerializer
from filters.models import Filter, Filtering
from elements.models import Channel, Slice, ChannelMap
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
        return self.settings

    def parse(self, request: Filtering, settings: dict) -> List[Tuple[str, Any]]:
        self.progress("Building Graph")
        array: xr.DataArray = request.representation.array

        filtered = self.filter(array, settings)

        repout, graph = Representation.distributed.from_xarray_and_request(filtered, request, name=f"{self.name} of {request.representation.name}")
        self.progress("Evaluating Graph")
        self.compute(graph)

        return [(repout, "create")]

    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        raise NotImplementedError


@register_consumer("maxisp",model= Filter)
class MaxISP(FilterConsumer):
    name = "Max ISP"
    path = "MaxISP"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Representation]

    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        return array.max(axis=3, keep_attrs=True)




@register_consumer("slicedmaxisp",model= Filter)
class SlicedMaxISP(FilterConsumer):
    name = "Sliced Max ISP"
    path = "SlicedMaxISP"
    settings = {"reload": True}
    inputs = [Representation, Slice]
    outputs = [Representation]


    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        print(array.z.size)

        lowerBound: int = int(settings.get("lowerBound",-1))
        upperBound: int = int(settings.get("upperBound",-1))

        array = array.sel(z=slice(lowerBound,upperBound)).max(dim="z")

        return array



@register_consumer("prewitt",model= Filter)
class PrewittFilter(FilterConsumer):
    name = "Prewitt"
    path = "Prewitt"
    settings = {"reload": True}
    inputs = [Representation, Channel]
    outputs = [Representation]

    def prepend(self, el, string= "Prewitt of"):
        items = el.channels.data.compute()
        for merge in items:
            merge["Name"] = f"{string} {merge['Name']}"
        return items

    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:
        it = array
        prewx = dask_image.ndfilters.prewitt(it.data, axis=0)
        prewy = dask_image.ndfilters.prewitt(it.data, axis=1)

        prewittfiltered = da.sqrt(prewx * prewx + prewy * prewy)

        c = self.prepend(it, string="Prewitt of")
        channels = xr.DataArray(da.array(c), dims="c")

        x = xr.DataArray(prewittfiltered, dims=it.dims, coords={ **it.coords, "channels": channels})

        return x


@register_consumer("mapping",model= Filter)
class Mapping(FilterConsumer):
    name = "Mapping"
    path = "Mapping"
    settings = {"reload": True}
    inputs = [Representation, ChannelMap]
    outputs = [Representation]

    def merge(self,channels: list, el):
        items = el.sel(c=channels).channels.data.compute()
        if len(items) == 1:
            return items[0]
        name = ",".join([item["Name"] for item in items])

        merge = items[0]
        merge["Index"] = -1
        merge["Name"] = f"Merged Channel ({name})"
        return merge


    def filter(self, array: xr.DataArray, settings: dict) -> xr.DataArray:



        threed = array

        rchannel = threed.sel(c=[1, 0])
        gchannel = threed.sel(c=[1, 0])
        bchannel = threed.sel(c=[0])

        rmeta = self.merge([1, 0], threed)
        gmeta = self.merge([1, 0], threed)
        bmeta = self.merge([0], threed)

        channels = xr.DataArray(da.from_array([rmeta, gmeta, bmeta]), dims=["c"])

        r = rchannel.max(dim="c", keepdims=True)
        g = gchannel.max(dim="c", keepdims=True)
        b = bchannel.max(dim="c", keepdims=True)

        x = da.concatenate([r.data, g.data, b.data], axis=2)
        x = xr.DataArray(x, dims=threed.dims, coords={**threed.coords, "channels": channels, "c": range(3)})

        return x
