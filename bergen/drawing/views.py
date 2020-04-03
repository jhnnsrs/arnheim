# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from drawing.models import LineROI
from drawing.serializers import LineROISerializer
from larvik.views import LarvikViewSet


class LineROIViewSet(LarvikViewSet):
    queryset = LineROI.objects.all()
    serializer_class = LineROISerializer
    publishers = [["nodeid",]]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("representation","creator")







