from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from strainers.models import Straining, Strainer
from strainers.serializers import StrainerSerializer, StrainingSerializer
from trontheim.viewsets import OsloActionViewSet


class StrainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Strainer.objects.all()
    serializer_class = StrainerSerializer



class StrainingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Straining.objects.all()
    serializer_class = StrainingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["representation"],["creator"],["roi"],["nodeid"]], "straining": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"
    actiontype = "startJob"

    def preprocess_jobs(self, serializer):
        strainer = Strainer.objects.get(pk=serializer.data["strainer"])
        print(strainer.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=strainer.channel)]




