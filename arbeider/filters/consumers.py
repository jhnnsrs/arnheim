from typing import Any, Dict, List, Tuple

import xarray as xr
from django.db import models

from elements.models import Channel, Slice, ChannelMap, Representation
from elements.serializers import RepresentationSerializer
from filters.logic.filters import Prewitt, Mapping
from filters.logic.projections import MaxISP, SlicedMaxISP
from filters.models import Filter, Filtering
from filters.serializers import FilteringSerializer
from larvik.consumers import DaskSyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.helpers import LarvikManager
from larvik.models import LarvikJob


class FilterConsumer(DaskSyncLarvikConsumer):
    type= "filter"
    unique = "notset"

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

        filtered = self.filter(array, settings, self)

        repout, graph = Representation.distributed.from_xarray_and_request(filtered, request,
                                                                           name=f"{self.name} of {request.representation.name}",
                                                                           type=self.unique,
                                                                           chain=f'{request.representation.chain}|{self.unique}')
        self.progress("Evaluating Graph")
        self.compute(graph)

        return [(repout, "create")]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        raise NotImplementedError


@register_consumer("maxisp",model= Filter)
class MaxISPConsumer(FilterConsumer):
    name = "Max ISP"
    path = "MaxISP"
    unique = "maxisp"
    settings = {"reload": True}
    inputs = [Representation]
    outputs = [Representation]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        return MaxISP.filter(array, settings, manager)






@register_consumer("slicedmaxisp",model= Filter)
class SlicedMaxISPConsumer(FilterConsumer):
    name = "Sliced Max ISP"
    path = "SlicedMaxISP"
    unique = "slicedmaxisp"
    settings = {"reload": True}
    inputs = [Representation, Slice]
    outputs = [Representation]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        return SlicedMaxISP.filter(array, settings, manager)



@register_consumer("prewitt",model= Filter)
class PrewittFilter(FilterConsumer):
    name = "Prewitt"
    path = "Prewitt"
    unique = "prewitt"
    settings = {"reload": True}
    inputs = [Representation, Channel]
    outputs = [Representation]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager ) -> xr.DataArray:
        return Prewitt.filter(array, settings, manager)



@register_consumer("mapping",model= Filter)
class MappingFilter(FilterConsumer):
    name = "Mapping"
    path = "Mapping"
    unique = "mapped"
    settings = {"reload": True}
    inputs = [Representation, ChannelMap]
    outputs = [Representation]

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        return Mapping.filter(array, settings, manager)



