from django.contrib.auth.models import User
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from social.models import Comment
from social.serializers import UserSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class CommentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MeViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        print(self.request.user)
        return self.request.user

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer_class()(self.get_object()).data)