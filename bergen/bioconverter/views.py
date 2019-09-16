from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from bioconverter.models import *
from bioconverter.serializers import *
from drawing.models import Sample
from drawing.serializers import SampleSerializer
from trontheim.viewsets import PublishingViewSet, channel_layer, OsloActionViewSet


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



class ConversionRequestViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = ConversionRequest.objects.all()
    serializer_class = ConversionRequestSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "representation": [("experiment", "sample", "creator")]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "bioconverter"
    actiontype = "convertsample"



class JobRequestOsloActionViewSet(OsloActionViewSet):
    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer
    publishers = [("experiment", "creator")]
    actionpublishers = {"sample": ("creator", "experiment"), "representation": ("experiment", "name")}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "test"
    actiontype = "convertsample"


class ConvertRequestOsloActionViewSet(OsloActionViewSet):
    queryset = ConvertToSampleRequest.objects.all()
    serializer_class = ConvertToSampleSerializer
    viewset_delegates = {"sample": [["creator"]]}
    publishers = [("experiment", "creator"),["creator"]]
    actionpublishers = {"sample": [("creator", "experiment","nodeid"),["experiment"]], "representation": [["creator"]]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "bioconverter"
    actiontype = "convertsample"

    def preprocess_jobs(self, serializer):
        serializer.data.pop("id")
        try:
            # A Sample ca be easily added via this approach and then with that in mind bExe serialized
            sampleserialized = SampleSerializer(data=serializer.data)
            if sampleserialized.is_valid():
                sample = sampleserialized.save()
                self.publishModel(sample,SampleSerializer,"create")

                conversionrequestserialized = ConversionRequestSerializer(data={"sample": sample.id, **serializer.data})
                print(conversionrequestserialized)
                print(conversionrequestserialized.is_valid())
                if conversionrequestserialized.is_valid():
                    conversionrequest = conversionrequestserialized.save()
                    print(conversionrequest)

                    # find the Converters path
                    converteritem = conversionrequest.converter
                    path = str(converteritem.channel)
                    # Right now this is defaulting to the standard

                    return [self.create_job(data=conversionrequestserialized.data,job=serializer.data)]
            return []
        except:
            return []


