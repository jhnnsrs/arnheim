# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from bioconverter.models import Analyzer
from bioconverter.serializers import *
from larvik.views import LarvikJobViewSet, LarvikViewSet


class ConverterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Converter.objects.all()
    serializer_class = ConverterSerializer


class ConversingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Conversing.objects.all()
    serializer_class = ConversingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("experiment",),("creator",),("nodeid",)], "representation": [("experiment", "sample", "creator"),("nodeid",)],"conversing": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "bioconverter"


class BioImageViewSet(LarvikViewSet):


    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","locker")
    queryset = BioImage.objects.all()
    serializer_class = BioImageSerializer
    publishers = [["experiment"],["locker"]]



class BioSeriesViewSet(LarvikViewSet):

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator", "locker", "bioimage")
    queryset = BioSeries.objects.all()
    serializer_class = BioSeriesSerializer
    publishers = [["experiment"]]

class LockerViewSet(LarvikViewSet):

    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    publishers = [["creator"]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)

class AnalyzingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","nodeid")
    queryset = Analyzing.objects.all()
    serializer_class = AnalyzingSerializer
    publishers = [["nodeid"]]
    actionpublishers = {"bioseries": [("locker",),("nodeid",)], "analyzing": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "biometa"
    actiontype = "startJob"

    def preprocess_jobs(self, serializer):
        return [self.create_job(data=serializer.data, job=serializer.data, channel=self.channel)]


class AnalyzerViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer


