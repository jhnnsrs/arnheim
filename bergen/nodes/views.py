from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from nodes.models import *
from nodes.serializers import *
from trontheim.viewsets import OsloViewSet


class NodeViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    publishers = [["variety"],["creator"]]



class NodeVarietyViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("host",)
    queryset = NodeVariety.objects.all()
    serializer_class = NodeVarietySerializer
    publishers = [["variety"],["creator"]]


class NodeElementViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = NodeElement.objects.all()
    serializer_class = NodeElementSerializer
    publishers = [["variety"],["creator"]]


class ArnheimHostViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ArnheimHost.objects.all()
    serializer_class = ArnheimHostSerializer
    publishers = [["variety"],["creator"]]