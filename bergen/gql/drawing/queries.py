import graphene
from graphene_django_extras import DjangoFilterListField

from .types import RoiType


class DrawingQueries(graphene.ObjectType):
    all_rois = DjangoFilterListField(RoiType)
