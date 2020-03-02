# Create your views here.

from larvik.views import LarvikViewSet, LarvikJobViewSet
from transformers.models import Transformer, Transforming
from transformers.serializers import TransformerSerializer, TransformingSerializer


class TransformerViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transformer.objects.all()
    serializer_class = TransformerSerializer


class TransformingViewSet(LarvikJobViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    queryset = Transforming.objects.all()[:100]
    serializer_class = TransformingSerializer
    publishers = [["sample"]]
    actionpublishers = {"sample": [("creator", "experiment")], "transformation": [["representation"],["creator"],["roi"],["nodeid"]], "transforming": [("nodeid",)]}
    # this publishers will be send to the Action Handles and then they can send to the according
    channel = "maxisp"

    def preprocess_jobs(self, serializer):
        transformer = Transformer.objects.get(pk=serializer.data["transformer"])
        print(transformer.channel)
        return [self.create_job(data=serializer.data,job=serializer.data,channel=transformer.channel)]







