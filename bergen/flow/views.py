from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from flow.models import ConversionFlow, FilterFlow
from flow.serializers import FlowSerializer, Flow, ConversionFlowSerializer, FilterFlowSerializer
from trontheim.viewsets import OsloViewSet


class FlowViewSet(OsloViewSet):

    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","group")
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    publishers = [["creator"]]


class FilterFlowViewSet(OsloViewSet):

    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","group","type")
    queryset = FilterFlow.objects.all()
    serializer_class = FilterFlowSerializer
    publishers = [["creator"]]

class ConversionFlowViewSet(OsloViewSet):

    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","group")
    queryset = ConversionFlow.objects.all()
    serializer_class = ConversionFlowSerializer
    publishers = [["creator"]]

