# Create your views here.
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from larvik.serializers import ZarrSerializer
from larvik.logging import get_module_logger
from larvik.models import Zarr
from larvik.utils import UUIDEncoder

channel_layer = get_channel_layer()

class LarvikJobWrapper(object):

    def __init__(self, data=None, actiontype=None, actionpublishers=None, job=None, channel=None):
        self.actiontype = actiontype
        self.data = data
        self.job = job if job else data
        self.actionpublishers = actionpublishers
        self.channel = channel

class LarvikViewSet(viewsets.ModelViewSet):
    # TODO: The stringpublishing is yet not working

    publishers = None
    viewset_delegates = None
    stringpublish = True


    def __init__(self, **kwargs):
        self.logger = get_module_logger(type(self).__name__)
        super().__init__(**kwargs)

    def publish(self, serializer, method):

        serializedData = serializer.data
        serializedData = json.loads(json.dumps(serializedData, cls=UUIDEncoder)) #Shit workaround to get UUUID to be string

        if self.publishers is not None:
            for el in self.publishers:
                modelfield = "empty"
                try:
                    path = ""
                    for modelfield in el:
                        try:
                            value = serializedData[modelfield]
                            path += "{0}_{1}_".format(str(modelfield), str(value))
                        except KeyError as e:
                            self.logger.info("Modelfield {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
                            self.logger.info("Publishing to String {0}".format(modelfield))
                            path += "{0}_".format(str(modelfield))
                    path = path[:-1]
                    self.logger.info("Publishing to Models {0}".format(path))
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": method, "data": serializedData})
                except KeyError as e:
                    self.logger.info("Error Babe !!!".format(str(el), str(self.serializer_class.__name__)))


    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.publish(serializer, "create")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.publish(serializer, "update")

    def perform_destroy(self, instance):
        serialized = self.serializer_class(instance)
        self.publish(serialized, "delete")
        super().perform_destroy(instance)


class LarvikJobViewSet(LarvikViewSet):
    actionpublishers = None  # this publishers will be send to the Action Handles and then they can send to the according
    channel = None
    actiontype = "startJob"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def preprocess_jobs(self, serializer):
        """ If you need to alter any data like creating an Model on the fly
         or create various jobs from one request, here is the place
         should return Array of Jobs that need executing"""
        return [self.create_job(serializer.data)]

    def create_job(self, data, actiontype=None, actionpublishers=None, job=None, channel=None) -> LarvikJobWrapper:
        actiontype = actiontype if actiontype else self.actiontype
        actionpublishers = actionpublishers if actionpublishers else self.actionpublishers
        job = job if job else data
        channel = channel if channel else self.channel
        return LarvikJobWrapper(data, actiontype, actionpublishers, job, channel)

    def perform_create(self, serializer):
        """ Right now only the creation of a new Job is possible, no way of stopping a job on its way"""
        serializer.save()
        jobs = self.preprocess_jobs(serializer)
        self.publish_jobs(jobs)
        self.publish(serializer, "create")

    def publish_jobs(self, jobs: [LarvikJobWrapper]):
        for nana in jobs:
            async_to_sync(channel_layer.send)(nana.channel, {"type": nana.actiontype, "data": nana.data,
                                                             "publishers": nana.actionpublishers, "job": nana.job})


class ZarrViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Zarr.objects.all()
    serializer_class = ZarrSerializer
    publishers = [["sample"]]
    filter_fields = ("group",)


    def zarrSelect(self,request):
        zarr: Zarr = self.get_object()
        query_params = request.query_params
        array = zarr.array
        # We are trying to pass on selection params
        array = self.queryselect(array, query_params)
        return array

    def queryselect(self, array, query_params):
        try:
            array = array.sel(channel=query_params["channel"]) if "channel" in query_params else array
        except Exception as e:
            return APIException(e)
        return array


    @action(methods=['get'], detail=True,
            url_path='shape', url_name='shape')
    def shape(self, request, pk):
        # We are trying to pass on selection params
        array = self.zarrSelect(request)

        answer = json.dumps(array.shape)
        response = HttpResponse(answer, content_type="application/json")
        return response



    @action(methods=['get'], detail=True,
            url_path='channels', url_name='channels')
    def channels(self, request, pk):
        # We are trying to pass on selection params
        array = self.zarrSelect(request)
        try:
            answer = array.biometa.channels.to_json(orient="records")
        except AttributeError as e:
            return HttpResponse(json.dumps([]), content_type="application/json")
        response = HttpResponse(answer, content_type="application/json")
        return response

    @action(methods=['get'], detail=True,
            url_path='values', url_name='values')
    def values(self, request, pk):
        # We are trying to pass on selection params
        array = self.zarrSelect(request)

        print(array.values)
        answer = json.dumps(list(array.values.tolist()))
        response = HttpResponse(answer, content_type="application/json")
        return response

    @action(methods=['get'], detail=True,
            url_path='planes', url_name='planes')
    def planes(self, request, pk):
        # We are trying to pass on selection params
        array = self.zarrSelect(request)
        try:
            answer = array.biometa.planes.to_json(orient="records")
        except AttributeError as e:
            return HttpResponse(json.dumps([]), content_type="application/json")
        response = HttpResponse(answer, content_type="application/json")
        return response