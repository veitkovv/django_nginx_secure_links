import graphene

from .api import file, user, secure_link, default_settings


class Query(user.Query,
            file.Query,
            secure_link.Query,
            default_settings.Query,
            graphene.ObjectType
            ):
    pass


class Mutation(user.Mutation,
               secure_link.Mutation,
               graphene.ObjectType
               ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
