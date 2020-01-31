# Create your views here.
import copy

from django.contrib.auth.hashers import get_hasher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from flow.models import Layout, Node, External, ExternalRequest
from flow.policies import ExternalAccessPolicy
from flow.serializers import FlowSerializer, Flow, NodeSerializer, LayoutSerializer, ExternalSerializer, \
    ExternalRequestSerializer, ExternalNewSerializer
from larvik.views import LarvikViewSet


class FlowViewSet(LarvikViewSet):
    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator", "group", "type")
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    publishers = [["creator"]]


class LayoutViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("flows",)
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializer
    publishers = [["creator"]]





class NodeViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    publishers = [["variety"], ["creator"]]


class ExternalViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = External.objects.all()
    permission_classes = (ExternalAccessPolicy,)
    serializer_class = ExternalSerializer
    publishers = [["creator","subset"]]

    @action(detail=False, )
    def recent(self, request):
        recent_externals = External.objects.filter(creator=request.user).order_by('-created_at')[:5]

        page = self.paginate_queryset(recent_externals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_externals, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False,
            url_path='new', url_name='new')
    def new(self, request):
        user = request.user
        hasher = get_hasher("default")
        nana = ExternalNewSerializer(data=request.data)
        if nana.is_valid():
            accesstoken = user.id  # TODO: THIS should be a unique string for every user, their own private secret
            uniqueexternalid = hasher.encode(accesstoken, nana.validated_data["name"])
        else:
            raise ValidationError("Something is wrong here")


        # Checking if this external already exists in Data
        external = External.objects.filter(uniqueid=uniqueexternalid)
        if not external.exists():
            newexternaldict = copy.copy(request.data)
            newexternaldict["uniqueid"] = uniqueexternalid
            newexternal = ExternalSerializer(data=newexternaldict)
            if newexternal.is_valid():
                instance = newexternal.save()
                self.publish(newexternal,"create")
                return Response(newexternal.data)
            else:
                raise ValidationError("You didnt provide the correct data")

        else:
            newexternal= ExternalSerializer(external.first())
            self.publish(newexternal,"update")
            return Response(newexternal.data)



class ExternalRequestViewSet(LarvikViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = ExternalRequest.objects.all()
    serializer_class = ExternalRequestSerializer
    publishers = [["external"]]
