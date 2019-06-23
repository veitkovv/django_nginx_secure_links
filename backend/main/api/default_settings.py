import graphene
from graphql_jwt.decorators import login_required

from django.conf import settings


class Query(graphene.ObjectType):
    min_url_expires = graphene.Int()
    max_url_expires = graphene.Int()

    @login_required
    def resolve_min_url_expires(self, info):
        return settings.MIN_PUBLIC_URL_TTL

    @login_required
    def resolve_max_url_expires(self, info):
        return settings.MAX_PUBLIC_URL_TTL


class UrlExpiresMutation(graphene.Mutation):
    class Arguments:
        new_url_expires = graphene.Int()

    ok = graphene.Boolean()
    new_url_expires = graphene.Int()

    @login_required
    def mutate(self, info, new_url_expires):
        info.context.user.profile.url_ttl = new_url_expires
        info.context.user.save()
        return UrlExpiresMutation(ok=True, new_url_expires=new_url_expires)


class Mutation:
    set_url_expires = UrlExpiresMutation.Field()
