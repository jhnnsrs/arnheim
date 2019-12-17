import json

import numpy as np

from biouploader.models import BioMeta
from drawing.models import ROI
from evaluators.logic.clusterAnalysis import findConnectedCluster
from evaluators.models import Evaluating, VolumeData, ClusterData, LengthData
from evaluators.serializers import DataSerializer, EvaluatingSerializer, VolumeDataSerializer, ClusterDataSerializer, \
    LengthDataSerializer
from evaluators.utils import get_evaluating_or_error, update_clusterdata_or_create, \
    update_lengthdata_or_create
from transformers.models import Transformation
from trontheim.consumers import OsloJobConsumer


class EvaluatingConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Evaluating = await get_evaluating_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.evaluator.defaultsettings)

        roi: ROI = request.roi
        transformation: Transformation = request.transformation
        meta: BioMeta = request.sample.meta

        datamodel = await self.parse(settings, transformation, roi, meta, request)
        datainstance, method = await self.getDataFunction()(request, datamodel, settings)


        await self.modelCreated(datainstance, DataSerializer, method)
        await self.modelCreated(datainstance, self.getSerializer(), method)

    async def parse(self, settings: dict, transformation: Transformation, roi: ROI, meta: BioMeta, evaluating: Evaluating) -> np.array:
        raise NotImplementedError

    def getDataFunction(self):
        raise NotImplementedError

    def getSerializer(self):
        raise NotImplementedError

    async def raiseError(self, error):
        self.data["error"] = error
        await self.modelCreated(self.data, EvaluatingSerializer, "update")

    async def getsettings(self, settings: str, defaultsettings: str):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = json.loads(defaultsettings)
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings



class LengthDataFromIntensityProfile(EvaluatingConsumer):

    def getSerializer(self):
        return LengthDataSerializer

    def getDataFunction(self):
        return update_lengthdata_or_create

    async def parse(self, settings: dict, transformation: Transformation, roi: ROI, meta: BioMeta, evaluating: Evaluating) -> np.array:

        threshold: float = float(settings["threshold"]) if "threshold" in settings else 0


        print("Hallloooo",threshold)



        intensity = transformation.numpy.get_array()
        print(intensity.shape)
        width = intensity.shape[1]

        # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
        physizex = meta.xphysical
        print(physizex)

        # Maybe user has defined different starts and ends
        userdefinedstart = int(settings["userdefinedstart"]) if "userdefinedstart" in settings else 0
        userdefinedend = int(settings["userdefinedend"]) if "userdefinedend" in settings else width
        # THIS PART CALCULATES THE ONCE OVER A CERTAIN THRESHOLD

        overindices = (intensity[:,0] > threshold).nonzero()[0]
        print(overindices)
        overindices = np.array([index for index in overindices if index >= userdefinedstart and index <= userdefinedend])

        print(overindices)
        try:
            xstart = overindices.min()
            ystart = overindices.max()

        except:
            xstart = -1
            ystart = -1


        aisstart = xstart
        aisend = ystart

        length = aisend - aisstart
        distancetostart = aisstart
        distancetoend = aisend

        physicallength = length * float(physizex)
        physicaldistancetostart= distancetostart * float(physizex)
        physicaldistancetoend= distancetoend * float(physizex)

        data = {}
        data["length"] = length
        data["distancetostart"] = distancetostart
        data["distancetoend"] = distancetoend
        data["physicallength"] = physicallength
        data["physicaldistancetostart"] = physicaldistancetostart
        data["physicaldistancetoend"] = physicaldistancetoend

        return data


class ClusterDataConsumer(EvaluatingConsumer):

    def getSerializer(self):
        return ClusterDataSerializer

    def getDataFunction(self):
        return update_clusterdata_or_create

    async def parse(self, settings: dict, transformation: Transformation, roi: ROI, meta: BioMeta, evaluating: Evaluating) -> np.array:

        array = transformation.numpy.get_array()
        cluster, n_cluster = findConnectedCluster(array, settings.get("sizeThreshold",3))
        n_pixels = sum(array.flat)
        areaphysical = n_pixels * meta.xphysical * meta.yphysical

        print("With Meta data of", str(meta.xphysical) + "and" + str(meta.yphysical))
        print("Creating Cluster of " + str(n_pixels) + " Pixels")
        print("Creating Cluster of " + str(areaphysical) + " Size")
        print("Creating Cluster of " + str(n_cluster) + " Cluster")

        data = {}
        data["clusternumber"] = n_cluster
        data["clusterareapixels"] = areaphysical
        data["clusterarea"] = areaphysical

        return data