import graphene

from .api import file, auth, secure_link


class Query(auth.Query,
            file.Query,
            secure_link.Query,
            graphene.ObjectType
            ):
    pass


class Mutation(auth.Mutation,
               secure_link.Mutation,
               graphene.ObjectType
               ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
