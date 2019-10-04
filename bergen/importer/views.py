# Create your views here.
from django.http import HttpResponse
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from pandas import DataFrame
from rest_framework import viewsets
from rest_framework.decorators import action

from importer.models import *
from importer.serializers import *
from trontheim.viewsets import OsloActionViewSet, OsloViewSet


class ImporterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Importer.objects.all()
    serializer_class = ImporterSerializer



class ImportingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Importing.objects.all()
    serializer_class = ImportingSerializer
    publishers = [["nodeid"]]
    actionpublishers = {"importing": [("creator",)], "bioimage": [["creator"], ["locker"]]}
    # this publishers will be send to the Action Handles and then they can send to the according
    actiontype = "startconverting"

    def preprocess_jobs(self, serializer):
        oracle = Importer.objects.get(pk=serializer.data["importer"])
        print(oracle.channel)
        return [self.create_job(data=serializer.data, job=serializer.data, channel=oracle.channel)]
