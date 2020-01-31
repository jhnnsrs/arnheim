# Create your views here.

from larvik.views import LarvikViewSet, LarvikJobViewSet
from strainers.models import Straining, Strainer
from strainers.serializers import StrainerSerializer, StrainingSerializer


class StrainerViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Strainer.objects.all()
    serializer_class = StrainerSerializer



class StrainingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Straining.objects.all()
    serializer_class = StrainingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["representation"],["creator"],["roi"],["nodeid"]], "straining": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"

    def preprocess_jobs(self, serializer):
        strainer = Strainer.objects.get(pk=serializer.data["strainer"])
        print(strainer.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=strainer.channel)]




