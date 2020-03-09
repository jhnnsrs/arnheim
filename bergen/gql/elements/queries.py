import graphene
from graphene_django_extras import DjangoFilterListField

from .types import ExperimentType, SampleType, RepresentationType


class ElementQueries(graphene.ObjectType):
    all_samples = DjangoFilterListField(SampleType,description='All Sample Filtered')
    all_experiments = DjangoFilterListField(ExperimentType,description='All Experiments Filtered')
    all_representations = DjangoFilterListField(RepresentationType,description='All Experiments Filtered')
