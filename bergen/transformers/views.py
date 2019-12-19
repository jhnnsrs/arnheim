from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from transformers.models import Transformer, Transforming, Transformation
from transformers.serializers import TransformerSerializer, TransformingSerializer, TransformationSerializer
from trontheim.viewsets import OsloActionViewSet


class TransformerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transformer.objects.all()
    serializer_class = TransformerSerializer




class TransformationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment", "creator", "roi","representation","sample")
    queryset = Transformation.objects.all()
    serializer_class = TransformationSerializer

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        try:
            transformation: Transformation = self.get_object()
            image_data = transformation.image.image
            response = HttpResponse(image_data, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(transformation.image.image.name)
            return response
        except:
            return HttpResponseRedirect("http://via.placeholder.com/1024x1024/000000/ffffff")


class TransformingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Transforming.objects.all()[:100]
    serializer_class = TransformingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["representation"],["creator"],["roi"],["nodeid"]], "transforming": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"
    actiontype = "startJob"

    def preprocess_jobs(self, serializer):
        transformer = Transformer.objects.get(pk=serializer.data["transformer"])
        print(transformer.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=transformer.channel)]







