from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from evaluators.models import Evaluator, Data, Evaluating, VolumeData
from evaluators.serializers import EvaluatorSerializer, DataSerializer, EvaluatingSerializer, VolumeDataSerializer
from trontheim.viewsets import OsloActionViewSet, OsloViewSet


class EvaluatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Evaluator.objects.all()
    serializer_class = EvaluatorSerializer


class DataViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    publishers = [["sample"],["transformation"]]


class VolumeDataViewSet(OsloViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ["transformation","roi"]
    queryset = VolumeData.objects.all()
    serializer_class = VolumeDataSerializer
    publishers = [["sample"],["transformation"]]


class EvaluatingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Evaluating.objects.all()
    serializer_class = EvaluatingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "data": [["transformation"],["creator"]], "volumedata": [["transformation"],["creator"],["roi"]]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"
    actiontype = "startparsing"

    def preprocess_jobs(self, serializer):
        evaluator = Evaluator.objects.get(pk=serializer.data["evaluator"])
        print(evaluator.channel)
        return [self.create_job(data=serializer.data, job=serializer.data, channel=evaluator.channel)]