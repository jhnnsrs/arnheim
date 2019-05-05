# Create your views here.
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect
from oauth2_provider.contrib.rest_framework import permissions, TokenHasScope
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

from drawing.models import Sample, ROI, Experiment, BioMeta
from drawing.serializers import SampleSerializer, RoiSerializer, ExperimentSerializer, BioMetaSerializer
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer

from trontheim.viewsets import PublishingViewSet, OsloViewSet
from django_filters.rest_framework import DjangoFilterBackend

class SampleViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [("experiment",),("creator",)]
    filter_fields = ("creator","experiment","bioseries")



class RoiViewSet(OsloViewSet):
    queryset = ROI.objects.all()
    serializer_class = RoiSerializer
    publishers = [["representation"],["creator"],["nodeid"]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation","sample","creator")

class BioMetaViewSet(OsloViewSet):
    queryset = BioMeta.objects.all()
    serializer_class = BioMetaSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("sample",)


class ExperimentViewSet(OsloViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    filter_backends = (DjangoFilterBackend,)
    publishers = [["creator"]]
    filter_fields = ("creator",)

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        experiment: Experiment = self.get_object()
        image_data = experiment.image
        response = HttpResponse(image_data, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(experiment.image.name)
        return response

class RepresentationViewSet(PublishingViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = (DjangoFilterBackend,)
    publishers = ["sample","creator"]
    filter_fields = ("sample",)

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        try:
            representation: Representation = self.get_object()
            image_data = representation.image.image
            response = HttpResponse(image_data, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(representation.image.image.name)
            return response
        except:
            return HttpResponseRedirect("http://via.placeholder.com/1024x1024/000000/ffffff")

    @action(methods=['get'], detail=True,
            url_path='asnifti', url_name='asnifti')
    def asnifti(self, request, pk):
        representation: Representation = self.get_object()
        filepath = representation.nifti.file
        image_data = open(filepath, 'rb')
        response = HttpResponse(image_data, content_type="application/gzip")
        response['Content-Disposition'] = 'inline; filename="' + filepath + '.nii.gz"'
        return response


    @action(methods=["get"], detail=False,
            url_path="bysample", url_name="bysample")
    def bysample(self,request):
        return HttpResponse("404")

