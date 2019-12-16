# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from flow.models import Layout, ForeignNodeRequest, Node, ForeignNodeStatus, External, ExternalRequest
from flow.policies import ExternalAccessPolicy
from flow.serializers import FlowSerializer, Flow, NodeSerializer, LayoutSerializer, ForeignNodeRequestSerializer, \
    ForeignNodeStatusSerializer, ExternalSerializer, ExternalRequestSerializer
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

class ExternalViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = External.objects.all()
    permission_classes = (ExternalAccessPolicy,)
    serializer_class = ExternalSerializer
    publishers = [["creator"]]

    @action(detail=False, )
    def recent(self, request):
        recent_externals = External.objects.filter(creator=request.user).order_by('-created_at')[:5]

        page = self.paginate_queryset(recent_externals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_externals, many=True)
        return Response(serializer.data)



class ExternalRequestViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = ExternalRequest.objects.all()
    serializer_class = ExternalRequestSerializer
    publishers = [["external"]]