# Create your views here.
from rest_framework import viewsets

from bioconverter.serializers import *
from trontheim.viewsets import OsloActionViewSet


class ConverterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Converter.objects.all()
    serializer_class = ConverterSerializer


class ConversingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Conversing.objects.all()
    serializer_class = ConversingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("experiment",),("creator",),("nodeid",)], "representation": [("experiment", "sample", "creator"),("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "bioconverter"
    actiontype = "convertseries"


