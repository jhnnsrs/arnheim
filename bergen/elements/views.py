# Create your views here.
# import the logging library
import logging

from django_filters.rest_framework import DjangoFilterBackend

from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Animal, FileMatchString, Representation, \
    Transformation, ROI
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer, \
    ExperimentalGroupSerializer, AnimalSerializer, FileMatchStringSerializer, RepresentationSerializer, ROISerializer
from larvik.views import LarvikViewSet

# Get an instance of a logger
from transformers.serializers import TransformationSerializer

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


class RepresentationViewSet(LarvikViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = (DjangoFilterBackend,)
    publishers = [["sample"],["creator"]]
    filter_fields = ("sample",)


class TransformationViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation",)
    queryset = Transformation.objects.all()
    serializer_class = TransformationSerializer


class RoiViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation",)
    queryset = ROI.objects.all()
    serializer_class = ROISerializer