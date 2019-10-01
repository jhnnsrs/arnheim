import graphene
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoFilterPaginateListField,DjangoFilterListField, LimitOffsetGraphqlPagination
from .types import ExperimentType, SampleType


class ElementQueries(graphene.ObjectType):
    all_samples = DjangoFilterListField(SampleType,description='All Sample Filtered')
    all_experiments = DjangoFilterListField(ExperimentType,description='All Experiments Filtered')
