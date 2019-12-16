# Create your views here.
import tempfile

import h5py
from django.http import HttpResponse
from django.utils.http import urlencode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Animal, FileMatchString, Numpy
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer, \
    ExperimentalGroupSerializer, AnimalSerializer, FileMatchStringSerializer, NumpySerializer
from hdfserver import idgetter
from hdfserver.idgetter import getDataSetUUIDforNumpy, queryDataSetUUID
from trontheim.viewsets import OsloViewSet
import requests
from django.utils.html import escape
# import the logging library
import logging
import urllib.parse
import os


# Get an instance of a logger
logger = logging.getLogger(__name__)

class AntibodyViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Antibody.objects.all()
    serializer_class = AntibodySerializer
    publishers = [["creator"]]

class FileMatchStringViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = FileMatchString.objects.all()
    serializer_class = FileMatchStringSerializer
    publishers = [["creator"]]

class AnimalViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    publishers = [["creator"],["experiment"]]
    filter_fields = ("creator", "name","experiment","experimentalgroup")

class ExperimentalGroupViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ExperimentalGroup.objects.all()
    serializer_class = ExperimentalGroupSerializer
    publishers = [["experiment"]]
    filter_fields = ("creator", "name", "experiment")


class NumpyViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Numpy.objects.all()
    serializer_class = NumpySerializer
    publishers = [["sample"]]
    filter_fields = ("sample",)


    @action(methods=['get'], detail=True,
            url_path='value', url_name='value')
    def value(self, request, pk):
        numpy: Numpy = self.get_object()
        query_params = request.query_params

        domain, datasetid = getDataSetUUIDforNumpy(numpy)

        # We are trying to pass on selection params
        query = "?select={0}".format(query_params["select"]) if "select" in query_params else ""
        logger.info("Passing on SelectQuery: {0}".format(query))

        answer = queryDataSetUUID(domain, datasetid,"/value" + query)
        response = HttpResponse(answer, content_type="application/json")
        return response

    @action(methods=['get'], detail=True,
            url_path='shape', url_name='shape')
    def shape(self, request, pk):
        numpy: Numpy = self.get_object()
        query_params = request.query_params

        domain, datasetid = getDataSetUUIDforNumpy(numpy)

        answer = queryDataSetUUID(domain, datasetid, "/shape")
        response = HttpResponse(answer, content_type="application/json")
        return response

    @action(methods=['get'], detail=True,
            url_path='type', url_name='type')
    def type(self, request, pk):
        numpy: Numpy = self.get_object()
        query_params = request.query_params

        domain, datasetid = getDataSetUUIDforNumpy(numpy)

        answer = queryDataSetUUID(domain, datasetid, "/type")
        response = HttpResponse(answer, content_type="application/json")
        return response








class SampleViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [("experiment",),("creator",),("nodeid",)]
    filter_fields = ("creator","experiment","bioseries","experimentalgroup","bioseries__bioimage","bioseries__bioimage__locker")


class ExperimentViewSet(OsloViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [["creator"]]
    filter_fields = ("creator",)
