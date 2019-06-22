import graphene
import graphql_jwt
import graphene_django

from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

from ..models import Profile


class User(graphene_django.DjangoObjectType):
    class Meta:
        model = get_user_model()


class ProfileType(graphene_django.DjangoObjectType):
    class Meta:
        model = Profile


class ProfileMutation(graphene.Mutation):
    class Arguments:
        url_ttl = graphene.Int()

    # The class attributes define the response of the mutation
    graphene.Field(ProfileType)

    def mutate(self, info, url_ttl):
        profile = Profile()
        # profile = info.context.user.profile
        print(profile)
        # Notice we return an instance of this mutation
        # return ProfileMutation(profile=profile)


class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_profiles = graphene.List(ProfileType)

    me = graphene.Field(User)
    profile = graphene.Field(ProfileType)

    @login_required
    @graphene.resolve_only_args
    def resolve_all_users(self):
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
# update_profile = ProfileMutation.Field()
