from typing import Dict, Any, Callable, Awaitable

import numpy as np
from django.db import models
from rest_framework import serializers

from elements.models import Sample
from evaluators.logic.clusterAnalysis import findConnectedCluster
from evaluators.models import Evaluating, Evaluator, ClusterData, LengthData
from evaluators.serializers import EvaluatingSerializer, ClusterDataSerializer, \
    LengthDataSerializer
from evaluators.utils import get_evaluating_or_error, lengthdata_update_or_create, clusterdata_update_or_create
from larvik.consumers import ModelFuncAsyncLarvikConsumer
from larvik.discover import register_consumer
from larvik.utils import update_status_on_larvikjob
from transformers.models import Transformation


@register_consumer("lengthdata", model= Evaluator)
class LengthDataFromIntensityProfile(ModelFuncAsyncLarvikConsumer):
    name = "Length Data"
    path = "LengthData"
    settings = {"reload": True}
    inputs = [Sample, Transformation]
    outputs = [LengthData]

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_evaluating_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return {"data": lengthdata_update_or_create
                }

    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return {"LengthData": LengthDataSerializer,
                "Evaluating": EvaluatingSerializer}

    async def parse(self, request: Evaluating, settings: dict) -> Dict[str, Any]:

        transformation = request.transformation
        meta = request.sample.meta
        threshold: float = float(settings.get("threshold", 0))

        self.logger.info("Using Threshold {0}".format(threshold))

        intensity = transformation.numpy.get_array()
        #print(intensity.shape)
        width = intensity.shape[1]

        # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
        physizex = meta.xphysical
        self.logger.info("Using Physicalsize {0}".format(physizex))

        # Maybe user has defined different starts and ends
        userdefinedstart = int(settings.get("userdefinedstart", 0))
        userdefinedend = int(settings.get("userdefinedend", width))
        # THIS PART CALCULATES THE ONCE OVER A CERTAIN THRESHOLD
        self.logger.info("Using Userdefinedarea between {0} and {1}".format(userdefinedstart, userdefinedend))
        overindices = (intensity[:, 0] > threshold).nonzero()[0]
        #print(overindices)
        overindices = np.array(
            [index for index in overindices if index >= userdefinedstart and index <= userdefinedend])

        #print(overindices)
        try:
            xstart = overindices.min()
            ystart = overindices.max()

        except:
            self.logger.error("No Items over Threshold found, length not evaluated")
            xstart = -1
            ystart = -1

        aisstart = xstart
        aisend = ystart

        length = aisend - aisstart
        distancetostart = aisstart
        distancetoend = aisend

        physicallength = length * float(physizex)
        physicaldistancetostart = distancetostart * float(physizex)
        physicaldistancetoend = distancetoend * float(physizex)

        data = {}
        data["length"] = length
        data["distancetostart"] = distancetostart
        data["distancetoend"] = distancetoend
        data["physicallength"] = physicallength
        data["physicaldistancetostart"] = physicaldistancetostart
        data["physicaldistancetoend"] = physicaldistancetoend

        return {"data": data}




@register_consumer("clusterdata", model= Evaluator)
class ClusterDataConsumer(ModelFuncAsyncLarvikConsumer):
    name = "Cluster Data"
    path = "ClusterData"
    settings = {"reload": True}
    inputs = [Sample, Transformation]
    outputs = [ClusterData]

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_evaluating_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return {"data": clusterdata_update_or_create
                }

    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        return {"ClusterData": ClusterDataSerializer,
                "Evaluating": EvaluatingSerializer}

    async def parse(self, request: Evaluating, settings: dict) -> Dict[str, Any]:
        transformation = request.transformation
        meta = request.sample.meta

        array = transformation.numpy.get_array()
        cluster, n_cluster = findConnectedCluster(array, settings.get("sizeThreshold", 3))
        n_pixels = sum(array.flat)
        areaphysical = n_pixels * meta.xphysical * meta.yphysical

        self.logger.info("With Meta data of " + str(meta.xphysical) + " and " + str(meta.yphysical))
        self.logger.info("Creating Cluster of " + str(n_pixels) + " Pixels")
        self.logger.info("Creating Cluster of " + str(areaphysical) + " Size")
        self.logger.info("Creating Cluster of " + str(n_cluster) + " Cluster")

        data = {}
        data["clusternumber"] = n_cluster
        data["clusterareapixels"] = areaphysical
        data["clusterarea"] = areaphysical

        return {"data": data}
