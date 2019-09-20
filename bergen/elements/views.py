# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from elements.models import Antibody, Sample, Experiment
from elements.serializers import AntibodySerializer, SampleSerializer, ExperimentSerializer
from trontheim.viewsets import OsloViewSet


class AntibodyViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Antibody.objects.all()
    serializer_class = AntibodySerializer
    publishers = [["creator"]]


class SampleViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [("experiment",),("creator",),("nodeid",)]
    filter_fields = ("creator","experiment","bioseries")


class ExperimentViewSet(OsloViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [["creator"]]
    filter_fields = ("creator",)
