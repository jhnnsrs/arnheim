from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from evaluators.models import ClusterData, Data


class DataType(DjangoObjectType):
    class Meta:
        model = Data
        description = "Data is providing access to Clusternumber,  "
        filter_fields = {
            "creator": ("exact",),
            "sample__name": ("icontains", "iexact"),
            "experiment__name": ("icontains", "iexact"),
        }

class ClusterDataType(DjangoObjectType):
    class Meta:
        model = ClusterData
        description = " ClusterData is providing access to Clusternumber,  "
        filter_fields = {
            "creator": ("exact",),
            "sample__name": ("icontains", "iexact"),
            "sample__experiment__name": ("icontains", "iexact"),
        }

