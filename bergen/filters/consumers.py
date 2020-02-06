from typing import Any, Dict, List, Tuple

import dask.array as da
import dask_image.ndfilters
import xarray as xr
from django.db import models

from bioconverter.models import Representation
from bioconverter.serializers import RepresentationSerializer
from elements.models import Channel, Slice, ChannelMap
from filters.filters import MaxISP, SlicedMaxISP, Prewitt, Mapping
from filters.models import Filter, Filtering
from filters.serializers import FilteringSerializer
from larvik.consumers import DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.helpers import LarvikParser, LarvikManager
from larvik.models import LarvikJob


class FilterConsumer(DaskSyncLarvikConsumer):
    type= "filter"

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

        filtered = self.filter( array, settings, self)

        repout, graph = Representation.distributed.from_xarray_and_request(filtered, request, name=f"{self.name} of {request.representation.name}")
        self.progress("Evaluating Graph")
        self.compute(graph)

        return [(repout, "create")]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager,) -> xr.DataArray:
        raise NotImplementedError


@register_consumer("maxisp",model= Filter)
class MaxISPConsumer(FilterConsumer, MaxISP):
    name = "Max ISP"
    path = "MaxISP"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Representation]




@register_consumer("slicedmaxisp",model= Filter)
class SlicedMaxISPConsumer(FilterConsumer, SlicedMaxISP):
    name = "Sliced Max ISP"
    path = "SlicedMaxISP"
    settings = {"reload": True}
    inputs = [Representation, Slice]
    outputs = [Representation]



@register_consumer("prewitt",model= Filter)
class PrewittFilter(FilterConsumer, Prewitt):
    name = "Prewitt"
    path = "Prewitt"
    settings = {"reload": True}
    inputs = [Representation, Channel]
    outputs = [Representation]



@register_consumer("mapping",model= Filter)
class MappingFilter(FilterConsumer, Mapping):
    name = "Mapping"
    path = "Mapping"
    settings = {"reload": True}
    inputs = [Representation, ChannelMap]
    outputs = [Representation]



