# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Animal, FileMatchString
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer, \
    ExperimentalGroupSerializer, AnimalSerializer, FileMatchStringSerializer
from trontheim.viewsets import OsloViewSet


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
