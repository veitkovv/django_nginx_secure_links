import graphene

from .api import file, auth


class Query(auth.Query,
            file.Query,
            graphene.ObjectType
            ):
    pass


class Mutation(auth.Mutation,
               file.Mutation,
               graphene.ObjectType
               ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
