import graphene
import graphql_jwt
import graphene_django
from django.contrib.auth import get_user_model


class User(graphene_django.DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    users = graphene.List(User)
    me = graphene.Field(User)

    @graphene.resolve_only_args
    def resolve_users(self):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        if not info.context.user.is_authenticated:
            return None
        else:
            return info.context.user


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
