from django.http import HttpResponse
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from larvik.views import LarvikViewSet, LarvikJobViewSet
from metamorphers.filters import DisplayFilter
from metamorphers.models import Metamorpher, Metamorphing, Display, Exhibit
from metamorphers.serializers import MetamorpherSerializer, MetamorphingSerializer, DisplaySerializer, \
    ExhibitSerializer


class DisplayViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DisplayFilter
    queryset = Display.objects.all()
    serializer_class = DisplaySerializer
    publishers = [["creator"]]


class ExhibitViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","representation__sample")
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer
    publishers = [["creator"]]

    @action(methods=['get'], detail=True,
            url_path='asnifti', url_name='asnifti')
    def asnifti(self, request, pk):
        exhibit: Exhibit = self.get_object()
        filepath = exhibit.nifti.file
        image_data = open(filepath, 'rb')
        response = HttpResponse(image_data, content_type="application/gzip")
        response['Content-Disposition'] = 'inline; filename="' + filepath + '.nii.gz"'
        return response

class MetamorpherViewSet(LarvikViewSet):
    """<
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Metamorpher.objects.all()
    serializer_class = MetamorpherSerializer


class MetamorphingViewSet(LarvikJobViewSet):
    '''Enables publishing to the cOsloActionViewSethannel Layed.
    Publishers musst be Provided'''
    queryset = Metamorphing.objects.all()
    serializer_class = MetamorphingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "display": [("sample",),("creator",),("nodeid",)], "exhibit": [("sample",),("creator",),("nodeid",)], "metamorphing": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according

    def preprocess_jobs(self, serializer):
        metamorpher = Metamorpher.objects.get(pk=serializer.data["metamorpher"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]
