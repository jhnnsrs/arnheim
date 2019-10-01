import graphene
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoFilterPaginateListField,DjangoFilterListField, LimitOffsetGraphqlPagination
from .types import ClusterDataType, DataType


class EvaluatorQueries(graphene.ObjectType):
    # Possible User list queries definitions
    #users = DjangoListObjectField(UserListType, description='All Users query')
    #users1 = DjangoFilterPaginateListField(UserType, pagination=LimitOffsetGraphqlPagination())
    clusterdata = DjangoFilterListField(ClusterDataType)
    data = DjangoFilterListField(DataType)
    #users3 = DjangoListObjectField(UserListType, filterset_class=UserFilter, description='All Users query')

    # Defining a query for a single user
    # The DjangoObjectField have a ID type input field, that allow filter by id and is't necessary to define resolve function
    #user = DjangoObjectField(UserType, description='Single User query')

    # Another way to define a query to single user

    # # Exist two ways to define single or list user queries with DjangoSerializerType
    # user_retrieve1, user_list1 = UserModelType.QueryFields(
    #     description='Some description message for both queries',
    #     deprecation_reason='Some deprecation message for both queries'
    # )
    # user_retrieve2 = UserModelType.RetrieveField(
    #     description='Some description message for retrieve query',
    #     deprecation_reason='Some deprecation message for retrieve query'
    # )
    # user_list2 = UserModelType.ListField(
    #     description='Some description message for list query',
    #     deprecation_reason='Some deprecation message for list query'