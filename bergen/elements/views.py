from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from elements.models import Antibody
from elements.serializers import AntibodySerializer
from trontheim.viewsets import OsloViewSet




class AntibodyViewSet(OsloViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Antibody.objects.all()
    serializer_class = AntibodySerializer
    publishers = [["creator"]]
