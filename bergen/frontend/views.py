from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from frontend.models import FrontEndNode
from frontend.serializers import FrontEndNodeSerializer
from trontheim.viewsets import OsloActionViewSet, OsloViewSet





class FrontEndNodeViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = FrontEndNode.objects.all()
    serializer_class = FrontEndNodeSerializer
    publishers = [["creator"],["sample"]]



