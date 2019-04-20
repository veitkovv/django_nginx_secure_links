import graphene

from .api import file


class Query(file.Query,
            graphene.ObjectType
            ):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
