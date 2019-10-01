from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from drawing.models import ROI
from elements.models import Experiment, Sample
from evaluators.models import ClusterData, Data


class RoiType(DjangoObjectType):
    class Meta:
        model = ROI
        description = "All the Rois"
        filter_fields = {
            "creator": ("exact",),
            "display__name": ("icontains", "iexact"),
        }


