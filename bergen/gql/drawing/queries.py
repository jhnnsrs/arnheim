import graphene
from graphene_django_extras import DjangoFilterListField

from .types import LineROIType


class DrawingQueries(graphene.ObjectType):
    all_lines = DjangoFilterListField(LineROIType)
