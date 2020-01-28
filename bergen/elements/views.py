# Create your views here.
import json
# import the logging library
import logging

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Animal, FileMatchString, Zarr
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer, \
    ExperimentalGroupSerializer, AnimalSerializer, FileMatchStringSerializer, ZarrSerializer
from larvik.views import LarvikViewSet

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AntibodyViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Antibody.objects.all()
    serializer_class = AntibodySerializer
    publishers = [["creator"]]

class FileMatchStringViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = FileMatchString.objects.all()
    serializer_class = FileMatchStringSerializer
    publishers = [["creator"]]

class AnimalViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    publishers = [["creator"],["experiment"]]
    filter_fields = ("creator", "name","experiment","experimentalgroup")

class ExperimentalGroupViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ExperimentalGroup.objects.all()
    serializer_class = ExperimentalGroupSerializer
    publishers = [["experiment"]]
    filter_fields = ("creator", "name", "experiment")



class SampleViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [("experiment",),("creator",),("nodeid",)]
    filter_fields = ("creator","experiment","bioseries","experimentalgroup","bioseries__bioimage","bioseries__bioimage__locker")


class ExperimentViewSet(LarvikViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [["creator"]]
    filter_fields = ("creator",)


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