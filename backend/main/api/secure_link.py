# -*- coding: utf-8 -*-
import graphene

from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType
from ..models import SecureLink, File
from graphql_relay.node.node import from_global_id


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


class SecureLinkMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        user_id = graphene.Int()
        file_id = graphene.ID()

    # The class attributes define the response of the mutation
    secure_link = graphene.Field(SecureLinkType)

    def mutate(self, info, user_id, file_id):
        # 0. Найти модели по входным ID
        user = get_user_model().objects.get(pk=user_id)
        _, id_ = from_global_id(file_id)
        file = File.objects.get(pk=id_)

        secure_link = SecureLink()

        # 1. связать юзера с моделью
        secure_link.user = user

        # 2. сгенерировать ссылку, связать с моделью
        secure_link.url = secure_link.generate_secure_link(file.filename)
        secure_link.save()

        # 3. связать файл с моделью
        file.secure_link = secure_link
        file.save()

        # Notice we return an instance of this mutation
        return SecureLinkMutation(secure_link=secure_link)


class Mutation:
    create_secure_link = SecureLinkMutation.Field()
