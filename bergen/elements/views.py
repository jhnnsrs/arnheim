# Create your views here.
import tempfile

import h5py
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Animal, FileMatchString, Numpy
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer, \
    ExperimentalGroupSerializer, AnimalSerializer, FileMatchStringSerializer, NumpySerializer
from hdfserver import idgetter
from trontheim.viewsets import OsloViewSet
import requests
from django.utils.html import escape
# import the logging library
import logging

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

class HDFException(APIException):
    status_code = 503
    default_detail = 'HDF Service malfunctioning temporarily, try again later.'
    default_code = 'service_unavailable'


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

        print(request.query_params)
        host = "hdfserver"
        port = 5000
        domain = "sample-{0}.h5files.{1}".format(numpy.sample.id,host)
        headers = { "host": domain}
        type = numpy.type
        vid = numpy.vid
        print( type, vid)
        print( domain)
        try:
            datasetid = idgetter.getUUIDByPath(domain, "/{0}/{1}".format(type, vid))
        except KeyError as e:
            logger.info("The File seems not to be updated Try updating")
            reg = 'http://' + host + ':' + str(port) + "/update/"
            updated = requests.get(reg, headers=headers)
            if updated.status_code == 200:
                datasetid = idgetter.getUUIDByPath(domain, "/{0}/{1}".format(type, vid))
            else:
                raise HDFException()

        print(datasetid)

        reg = 'http://' + host + ':' + str(port) + "/datasets/" + datasetid + "/value"
        headers = { "host": domain}
        answer = requests.get(reg, headers= headers)
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
