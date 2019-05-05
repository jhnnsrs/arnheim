from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from filterbank.models import Parsing, Filter, Representation, Filtering
from filterbank.serializers import ParsingSerializer, FilterSerializer, RepresentationSerializer, FilteringSerializer
from trontheim.viewsets import PublishingViewSet, channel_layer, OsloActionViewSet


class FilterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer

class FilteringViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment",)
    queryset = Filtering.objects.all()
    serializer_class = FilteringSerializer
    publishers = [["experiment"]]
    actiontype = "startparsing"
    actionpublishers = {"representation": [("sample",),("creator",),("nodeid",)],"filtering": [("sample",),("creator",)]}

    def preprocess_jobs(self, serializer):
        filter = Filter.objects.get(pk=serializer.data["filter"])
        print(filter.channel)
        return [self.create_job(data=serializer.data, job=serializer.data, channel=filter.channel)]

class ParsingRequestViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Parsing.objects.all()
    serializer_class = ParsingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "representation": [("sample",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"
    actiontype = "startparsing"

    def preprocess_jobs(self, serializer):
        filter = Filter.objects.get(pk=serializer.data["filter"])
        print(filter.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=filter.channel)]




