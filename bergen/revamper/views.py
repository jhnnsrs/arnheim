from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from revamper.models import Mask, Revamper, Revamping
from revamper.serializers import MaskSerializer, RevamperSerializer, RevampingSerializer
from trontheim.viewsets import OsloActionViewSet, OsloViewSet


class MaskViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ["creator",]
    queryset = Mask.objects.all()
    serializer_class = MaskSerializer
    publishers = [["creator"],["sample"],["nodeid"]]



class RevamperViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Revamper.objects.all()
    serializer_class = RevamperSerializer


class RevampingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Revamping.objects.all()
    serializer_class = RevampingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["creator"],["roi"],["nodeid"]]}
    actiontype = "startconverting"

    def preprocess_jobs(self, serializer):
        metamorpher = Revamper.objects.get(pk=serializer.data["revamper"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]