# Create your views here.

from django.http import HttpResponseRedirect
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from larvik.views import LarvikViewSet, LarvikJobViewSet
from trontheim.viewsets import OsloActionViewSet
from visualizers.serializers import *


class VisualizerViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Visualizer.objects.all()
    serializer_class = VisualizerSerializer

class ProfileViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_fields = ["creator", "answer"]

    @action(methods=['get'], detail=True,
            url_path='html', url_name='html')
    def to_html(self, request, pk):
        profile: Profile = self.get_object()
        return HttpResponseRedirect(profile.htmlfile.url)

class ExcelExportViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ExcelExport.objects.all()
    serializer_class = ExcelExportSerializer
    filter_fields = ["creator", "answer"]

    @action(methods=['get'], detail=True,
            url_path='excel', url_name='excel')
    def to_excel(self, request, pk):
        profile: ExcelExport = self.get_object()
        return HttpResponseRedirect(profile.excelfile.url)



class VisualizingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Visualizing.objects.all()
    serializer_class = VisualizingSerializer
    publishers = [["creator"]]
    actionpublishers = {"visualizing": [("creator",)],
                        "profile": [["creator"], ["nodeid"],["answer"]],
                        "excelexport": [["creator"], ["nodeid"],["answer"]],
                        }
    # this publishers will be send to the Action Handles and then they can send to the according

    def preprocess_jobs(self, serializer):
        visualizer = Visualizer.objects.get(pk=serializer.data["visualizer"])
        print(visualizer.channel)
        return [self.create_job(data=serializer.data, job=serializer.data, channel=visualizer.channel)]
