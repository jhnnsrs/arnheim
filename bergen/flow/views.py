# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from flow.models import Layout, ForeignNodeRequest, Node, ForeignNodeStatus
from flow.serializers import FlowSerializer, Flow, NodeSerializer, LayoutSerializer, ForeignNodeRequestSerializer, \
    ForeignNodeStatusSerializer
from trontheim.viewsets import OsloViewSet


class FlowViewSet(OsloViewSet):

    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator","group","type")
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    publishers = [["creator"]]


class LayoutViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("flows",)
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializer
    publishers = [["creator"]]


class ForeignNodeRequestViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ForeignNodeRequest.objects.all()
    serializer_class = ForeignNodeRequestSerializer
    publishers = [["nodeid"]]

class ForeignNodeStatusViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ForeignNodeStatus.objects.all()
    serializer_class = ForeignNodeStatusSerializer
    publishers = [["creator"],["nodes_for_foreign"]]



class NodeViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    publishers = [["variety"],["creator"]]