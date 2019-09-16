from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from metamorphers.models import Metamorpher, Metamorphing, Display, Exhibit, Kafkaing
from metamorphers.serializers import MetamorpherSerializer, MetamorphingSerializer, DisplaySerializer, \
    ExhibitSerializer, KafkaingSerializer
from trontheim.viewsets import OsloActionViewSet, OsloViewSet


class DisplayViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment","creator","representation","sample")
    queryset = Display.objects.all()
    serializer_class = DisplaySerializer
    publishers = [["creator"],["sample"]]

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        try:
            display: Display = self.get_object()
            image_data = display.image
            response = HttpResponse(image_data, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(display.image.name)
            return response
        except:
            return HttpResponseRedirect("http://via.placeholder.com/1024x1024/000000/ffffff")

    @action(methods=['get'], detail=True,
            url_path='asnifti', url_name='asnifti')
    def asnifti(self, request, pk):
        representation: Display = self.get_object()
        filepath = representation.nifti.file
        image_data = open(filepath, 'rb')
        response = HttpResponse(image_data, content_type="application/gzip")
        response['Content-Disposition'] = 'inline; filename="' + filepath + '.nii.gz"'
        return response


class ExhibitViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment","creator","sample")
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer
    publishers = [["creator"],["sample"]]

    @action(methods=['get'], detail=True,
            url_path='asnifti', url_name='asnifti')
    def asnifti(self, request, pk):
        exhibit: Exhibit = self.get_object()
        filepath = exhibit.nifti.file
        image_data = open(filepath, 'rb')
        response = HttpResponse(image_data, content_type="application/gzip")
        response['Content-Disposition'] = 'inline; filename="' + filepath + '.nii.gz"'
        return response

class MetamorpherViewSet(viewsets.ModelViewSet):
    """<
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Metamorpher.objects.all()
    serializer_class = MetamorpherSerializer


class MetamorphingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Metamorphing.objects.all()
    serializer_class = MetamorphingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "display": [("sample",),("creator",),("nodeid",)], "exhibit": [("sample",),("creator",),("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    actiontype = "startconverting"

    def preprocess_jobs(self, serializer):
        metamorpher = Metamorpher.objects.get(pk=serializer.data["metamorpher"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]


class KafkaingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Kafkaing.objects.all()
    serializer_class = KafkaingSerializer
    # this publishers will be send to the Action Handles and then they can send to the according
    actiontype = "startconverting"
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "display": [("sample",), ("creator",), ("nodeid",)],
                        "exhibit": [("sample",), ("creator",), ("nodeid",)]}
    channel = "kafka"

    def preprocess_jobs(self, serializer):
        return [self.create_job(data=serializer.data,job=serializer.data,channel="kafka")]