import json

import javabridge as javabridge
import bioformats
import numpy as np
from channels.consumer import SyncConsumer, AsyncConsumer

from chat.logic.bioparser import loadBioMetaSeriesFromFile, loadBioImageSeriesFromFile
from filterbank.addins import toimage
from filterbank.models import Parsing, Representation, Filtering
from filterbank.serializers import RepresentationSerializer, FilteringSerializer
from filterbank.utils import  get_inputrepresentationbynode_or_error, get_filtering_or_error, \
    update_outputrepresentationbynode_or_create
from trontheim.consumers import OsloJobConsumer


class FilterConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Filtering = await get_filtering_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.filter.defaultsettings)
        inputrep, array = await get_inputrepresentationbynode_or_error(request)

        meta = json.loads(inputrep.meta)
        request.progress = 20
        await self.modelCreated(request, FilteringSerializer, "update")
        parsedarray, newmeta = await self.parse(settings,array,meta)

        ## This could be handled in the parsing function itself
        request.progress = 40
        await self.modelCreated(request, FilteringSerializer, "update")
        outputrep, method = await update_outputrepresentationbynode_or_create(request, parsedarray, inputrep, settings, newmeta)

        await self.modelCreated(outputrep, RepresentationSerializer, method)

    async def parse(self, filtersettings: dict,numpyarray: np.array, meta: dict) -> np.array:
        raise NotImplementedError


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




class MaxISP(FilterConsumer):
    async def parse(self, filtersettings: dict, numpyarray: np.array, meta: dict) -> np.array:
        array = numpyarray
        if len(array.shape) == 5:
            array = np.nanmax(array[:,:,:3,:,0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:,:,:3,:], axis=3)
        if len(array.shape) == 3:
            array = array[:,:,:3]
        if len(array.shape) == 2:
            array = array[:,:]

        return array, meta


class SlicedMaxISP(FilterConsumer):
    async def parse(self, filtersettings: dict, numpyarray: np.array, meta: dict) -> np.array:

        lowerBound: int = int(filtersettings["lowerBound"])
        upperBound: int = int(filtersettings["upperBound"])


        array = numpyarray
        if len(array.shape) == 5:
            array = np.nanmax(array[:,:,:3,lowerBound:upperBound,0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:,:,:3,lowerBound:upperBound], axis=3)
        if len(array.shape) == 3:
            array = array[:,:,:3]
        if len(array.shape) == 2:
            array = array[:,:]

        return array, meta


class PrewittFilter(FilterConsumer):
    async def parse(self, filtersettings: dict, numpyarray: np.array, meta: dict) -> np.array:
        import cv2

        array = numpyarray
        if len(array.shape) == 5:
            array = np.nanmax(array[:,:,:3,:,0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:,:,:3,:], axis=3)
        if len(array.shape) == 3:
            array = array[:,:,:3]

        if len(array.shape) == 2:
            gray = array
        else:
            gray = array[:, :, 0] #TODO: read from settings

        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

        img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
        img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
        img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)

        images = img_prewittx + img_prewitty
        return images, meta


class Mapping(FilterConsumer):
    async def parse(self, filtersettings: dict, numpyarray: np.array, meta: dict) -> np.array:

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
        return mappedfile, meta
