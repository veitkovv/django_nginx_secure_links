import json
import graphene
from django.conf import settings


class Query(graphene.ObjectType):
    default_settings = graphene.JSONString()
    min_ttl = graphene.Int()
    max_ttl = graphene.Int()

    def resolve_default_settings(self, info):
        default_settings = dict()
        default_settings['minTtl'] = settings.MIN_PUBLIC_URL_TTL
        default_settings['maxTtl'] = settings.MAX_PUBLIC_URL_TTL
        return json.dumps(default_settings)
