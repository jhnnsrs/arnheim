# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from larvik.views import LarvikViewSet, LarvikJobViewSet
from revamper.models import Mask, Revamper, Revamping
from revamper.serializers import MaskSerializer, RevamperSerializer, RevampingSerializer


class MaskViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ["creator",]
    queryset = Mask.objects.all()
    serializer_class = MaskSerializer
    publishers = [["creator"],["sample"],["nodeid"]]



class RevamperViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Revamper.objects.all()
    serializer_class = RevamperSerializer


class RevampingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Revamping.objects.all()
    serializer_class = RevampingSerializer
    publishers = [["creator"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["creator"],["roi"],["nodeid"]]}

    def preprocess_jobs(self, serializer):
        metamorpher = Revamper.objects.get(pk=serializer.data["revamper"])
        print(metamorpher.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=metamorpher.channel)]