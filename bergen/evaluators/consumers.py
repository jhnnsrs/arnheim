import json

import numpy as np

from biouploader.models import BioMeta
from drawing.models import ROI
from evaluators.logic.clusterAnalysis import findConnectedCluster
from evaluators.models import Evaluating, VolumeData, ClusterData
from evaluators.serializers import DataSerializer, EvaluatingSerializer, VolumeDataSerializer, ClusterDataSerializer
from evaluators.utils import get_evaluating_or_error, update_volumedata_or_create, update_clusterdata_or_create
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
        volumedata, method = await self.getDataFunction()(request, datamodel, settings)


        await self.modelCreated(volumedata, DataSerializer, method)
        await self.modelCreated(volumedata, self.getSerializer(), method)

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


class VolumetricDataConsumer(EvaluatingConsumer):

    async def parse(self, settings: dict, transformation: Transformation, roi: ROI, meta: BioMeta, evaluating: Evaluating) -> np.array:
        data = {"length": 4, "name": "Peter"}
        return data


class AISDataConsumer(EvaluatingConsumer):

    def getSerializer(self):
        return VolumeDataSerializer

    def getDataFunction(self):
        return update_volumedata_or_create

    async def parse(self, settings: dict, transformation: Transformation, roi: ROI, meta: BioMeta, evaluating: Evaluating) -> np.array:

        vectorlength: float = None
        b4channel: int = int(settings["b4channel"])
        threshold: float = float(settings["threshold"])
        tags: list = ["AIS"]

        transformation_image = transformation.numpy.get_array()
        vectorlength = 4 #TODO: Make this accurate
        height = 0
        width = 0
        channels = 0
        ndim = 2

        if len(transformation_image.shape) > 3 or len(transformation_image.shape) < 2:
            await self.raiseError("This is not a valid transformation. Shape exceeds the available dimensions")
            return
        if len(transformation_image.shape) == 3:
            height, width, channels = transformation_image.shape
            ndim = 3
        if len(transformation_image.shape) == 2:
            height, width = transformation_image.shape
            channels = 0
            ndim = 2

        # Maybe user has defined different starts and ends
        userdefinedstart = int(settings["userdefinedstart"]) if "userdefinedstart" in settings else 0
        userdefinedend = int(settings["userdefinedend"]) if "userdefinedend" in settings else width


        # this takes the middle part of the picture
        middleup = int((height / 2) - (height / 4))
        middledown = int((height / 2) + (height / 4))


        # trimm image according to needs
        if ndim == 3:
            trimmedimage = transformation_image[middleup:middledown, :, :]
        else:
            trimmedimage = transformation_image[middleup:middledown, :]

        np.seterr(divide='ignore', invalid='ignore')  # error level if a pixelvalue is 0
        averages = np.max(trimmedimage, axis=0)
        intensity = averages / averages.max(axis=0)

        # A JSON Serializiable version of our intensitycurves
        intensities = intensity.tolist()
        intensitycurves: str = json.dumps(intensities)

        # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
        physizex = meta.xphysical

        # THIS PART CALCULATES THE ONCE OVER A CERTAIN THRESHOLD
        if channels != 0:
            c = b4channel if b4channel < intensity.shape[1] else intensity.shape[1] - 1

            overindices = (intensity[:, c] > threshold).nonzero()[0]
        else:
            overindices = (intensity > threshold).nonzero()[0]

        overindices = np.array([index for index in overindices if index >= userdefinedstart and index <= userdefinedend])

        try:
            xstart = overindices.min()
            ystart = overindices.max()

        except:
            xstart = -1
            ystart = -1

            tags.append("Error")

        aisstart = xstart
        aisend = ystart
        pixellength = ystart - xstart

        physicallength = pixellength * float(physizex)

        data = VolumeData(roi=roi,
                          transformation=transformation,
                          sample=transformation.sample,
                          experiment=transformation.experiment,
                          b4channel=b4channel,
                          vectorlength=vectorlength,
                          pixellength=pixellength,
                          aisstart=aisstart,
                          aisend=aisend,
                          userdefinedstart=userdefinedstart,
                          userdefinedend=userdefinedend,
                          threshold=threshold,
                          physicallength=physicallength,
                          tags=",".join(tags),
                          intensitycurves=intensitycurves,
                          meta=meta,
                          nodeid=evaluating.nodeid)

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
        data = ClusterData(roi=roi,
                          transformation=transformation,
                          sample=transformation.sample,
                          experiment=transformation.experiment,
                          clusternumber= n_cluster,
                          clusterareapixels = n_pixels,
                          clusterarea = areaphysical,
                          spatialunit= meta.spacial_units+"²",
                          tags=",".join(["Cluster"]),
                          meta=meta,
                          nodeid=evaluating.nodeid)

        return data