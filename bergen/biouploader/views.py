from asgiref.sync import async_to_sync
from django.http import JsonResponse


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from biouploader.models import BioImage, BioSeries, Analyzing, Analyzer, Locker, BioMeta
from biouploader.serializers import BioImageSerializer, BioSeriesSerializer, AnalyzingSerializer, AnalyzerSerializer, \
    LockerSerializer, BioMetaSerializer
from biouploader.upload_utils import upload_file
from trontheim.viewsets import OsloViewSet, OsloActionViewSet, channel_layer

class BioImageViewSet(OsloViewSet):

    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","locker")
    queryset = BioImage.objects.all()
    serializer_class = BioImageSerializer
    publishers = [["experiment"],["locker"]]



class BioSeriesViewSet(OsloViewSet):

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator", "locker", "bioimage")
    queryset = BioSeries.objects.all()
    serializer_class = BioSeriesSerializer
    publishers = [["experiment"]]

class LockerViewSet(OsloViewSet):

    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    publishers = [["creator"]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)

class AnalyzingViewSet(OsloActionViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("experiment",)
    queryset = Analyzing.objects.all()
    serializer_class = AnalyzingSerializer
    publishers = [["nodeid"]]
    actionpublishers = {"bioseries": [("experiment",),("creator",),("locker",),("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "analyzer"
    actiontype = "startparsing"

    def preprocess_jobs(self, serializer):
        return [self.create_job(data=serializer.data, job=serializer.data, channel=self.channel)]


class AnalyzerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer


## THIS IS THE UPLOAD SECTION
@csrf_exempt
def upload_complete(request):
    '''view called on /upload/complete after nginx upload module finishes.
       1. nginx module uses /upload
       2. callback comes here with multipart form fields below!
    '''

    if request.method == "POST":

        path = request.POST.get('file.path')
        size = request.POST.get('file.size')
        filename = request.POST.get('name')
        version = request.POST.get('file.md5')
        creator = request.POST.get('creator')
        experiment = request.POST.get('experiment')
        locker = request.POST.get('locker')

        # You should implement some sort of authorization check here!

        # Expected params are upload_id, name, md5, and cid
        bioimage = upload_file(version = version,
                    path = path,
                    name = filename,
                    size = size,
                    experiment= experiment,
                    locker = locker,
                    creator= creator)

        # Redirect to main view if not terminal
        serializer = BioImageSerializer(bioimage)
        creator = serializer.data["creator"]
        print(serializer.data)
        async_to_sync(channel_layer.group_send)(
            "locker_{0}".format(locker),
            {
                "type": "stream",
                "stream": "bioimage",
                "room": "locker_{0}".format(locker),
                "method": "create",
                "data": serializer.data
            }
        )
        async_to_sync(channel_layer.group_send)(
            "creator_{0}".format(creator),
            {
                "type": "stream",
                "stream": "bioimage",
                "room": "creator_{0}".format(creator),
                "method": "create",
                "data": serializer.data
            }
        )

        return JsonResponse({"message":"Upload Complete"})

    return JsonResponse({"message":"No Data sent Complete"})


class BioMetaViewSet(OsloViewSet):
    queryset = BioMeta.objects.all()
    serializer_class = BioMetaSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("sample",)