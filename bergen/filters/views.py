from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from filters.models import Filter, Filtering
from filters.serializers import FilterSerializer, FilteringSerializer
from larvik.views import LarvikViewSet, LarvikJobViewSet


class FilterViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer




class FilteringViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("nodeid","creator")
    queryset = Filtering.objects.all()
    serializer_class = FilteringSerializer
    actionpublishers = {"representation": [("sample",),("creator",),("nodeid",)],"filtering": [("sample",),("creator",),("nodeid",)]}

    def preprocess_jobs(self, serializer):
        filter = Filter.objects.get(pk=serializer.data["filter"])
        print(filter.channel)
        return [self.create_job(data=serializer.data, job=serializer.data, channel=filter.channel)]