from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from mutaters.models import *
from mutaters.serializers import *
from trontheim.viewsets import OsloActionViewSet, OsloViewSet


class ReflectionViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment","creator","roi")
    queryset = Reflection.objects.all()
    serializer_class = ReflectionSerializer
    publishers = [["creator"],["sample"]]

    @action(methods=['get'], detail=True,
            url_path='asimage', url_name='asimage')
    def asimage(self, request, pk):
        try:
            reflection: Reflection = self.get_object()
            image_data = reflection.image
            response = HttpResponse(image_data, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(reflection.image.name)
            return response
        except:
            return HttpResponseRedirect("http://via.placeholder.com/1024x1024/000000/ffffff")


class MutaterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Mutater.objects.all()
    serializer_class = MutaterSerializer


class MutatingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Mutating.objects.all()
    serializer_class = MutatingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "reflection": [["creator"],["roi"],["nodeid"]]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "image"
    actiontype = "startconverting"

    def preprocess_jobs(self, serializer):
        metamorpher = Mutater.objects.get(pk=serializer.data["mutater"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]


