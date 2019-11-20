from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from elements.models import Experiment, Sample, ExperimentalGroup
from evaluators.models import ClusterData, Data


class ExperimentType(DjangoObjectType):
    class Meta:
        model = Experiment
        description = "All the Experiments  "
        filter_fields = {
            "creator": ("exact",),
            "description": ("icontains", "iexact"),
            "name": ("icontains", "iexact"),
        }
        exclude_fields = ['tags']


class SampleType(DjangoObjectType):
    class Meta:
        model = Sample
        description = " All the Samples stored in Oslo "
        filter_fields = {
            "creator": ("exact",),
            "experiment__name": ("icontains", "iexact"),
            "bioseries__name": ("icontains", "iexact"),
        }


class ExperimentalGroupType(DjangoObjectType):
    class Meta:
        model = ExperimentalGroup
        description = " All the ExperimentalGroups stored in Oslo "
        filter_fields = {
            "creator": ("exact",),
        }

