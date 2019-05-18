# -*- coding: utf-8 -*-
import graphene
from graphene_django.types import DjangoObjectType
from ..models import SecureLink


class SecureLinkType(DjangoObjectType):
    class Meta:
        model = SecureLink


class Query(object):
    secure_link = graphene.Field(SecureLinkType)
    all_secure_links = graphene.List(SecureLinkType)

    def resolve_all_secure_links(self, info, **kwargs):
        return SecureLink.objects.all()

    def resolve_secure_link(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SecureLink.objects.get(pk=id)
