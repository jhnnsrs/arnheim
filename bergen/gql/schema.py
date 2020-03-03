import graphene
from django.contrib.auth.models import User
from graphene_django_extras import DjangoObjectField, all_directives
from graphene_django_extras import DjangoObjectType

from gql.drawing.queries import DrawingQueries
from gql.elements.queries import ElementQueries
from gql.evaluators.queries import EvaluatorQueries
from gql.bioconverter.queries import BioConverterQueries


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(EvaluatorQueries,
            ElementQueries,
            DrawingQueries,
            BioConverterQueries,
            graphene.ObjectType):
    user = DjangoObjectField(UserType, description='Single User query')


schema = graphene.Schema(query=Query,directives=all_directives)
