import graphene
from graphene_django_extras import DjangoFilterListField

from .types import BioSeriesType, BioImageType


class BioConverterQueries(graphene.ObjectType):
    all_bioseries = DjangoFilterListField(BioSeriesType)
    all_bioimages = DjangoFilterListField(BioImageType)
