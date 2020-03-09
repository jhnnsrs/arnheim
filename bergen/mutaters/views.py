from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from larvik.views import LarvikViewSet, LarvikJobViewSet
from mutaters.serializers import *


class ReflectionViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("transformation",)
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


class MutaterViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Mutater.objects.all()
    serializer_class = MutaterSerializer


class MutatingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Mutating.objects.all()
    serializer_class = MutatingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "reflection": [["creator"],["roi"],["nodeid"]]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "image"

    def preprocess_jobs(self, serializer):
        metamorpher = Mutater.objects.get(pk=serializer.data["mutater"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]


