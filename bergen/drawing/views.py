# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from bioconverter.models import Representation
from bioconverter.serializers import RepresentationSerializer
from drawing.models import ROI
from drawing.serializers import RoiSerializer
from larvik.views import LarvikViewSet
from trontheim.viewsets import OsloViewSet


class RoiViewSet(LarvikViewSet):
    queryset = ROI.objects.all()
    serializer_class = RoiSerializer
    publishers = [["representation"],["creator"],["sample"],["sample","display"]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation","sample","creator","display")


class RepresentationViewSet(LarvikViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = (DjangoFilterBackend,)
    publishers = [["sample"],["creator"]]
    filter_fields = ("sample",)





