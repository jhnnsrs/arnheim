# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from bioconverter.models import Representation
from bioconverter.serializers import RepresentationSerializer
from drawing.models import ROI
from drawing.serializers import RoiSerializer
from trontheim.viewsets import OsloViewSet


class RoiViewSet(OsloViewSet):
    queryset = ROI.objects.all()
    serializer_class = RoiSerializer
    publishers = [["representation"],["creator"],["nodeid"],["sample"]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation","sample","creator")


class RepresentationViewSet(OsloViewSet):

    queryset = Representation.objects.all()
    serializer_class = RepresentationSerializer
    filter_backends = (DjangoFilterBackend,)
    publishers = [["sample"],["creator"]]
    filter_fields = ("sample",)


