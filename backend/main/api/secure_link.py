# -*- coding: utf-8 -*-
import graphene

from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
from graphql_jwt.decorators import login_required

from ..models import SecureLink, File


class SecureLinkType(DjangoObjectType):
    class Meta:
        model = SecureLink

    link_deadline = graphene.DateTime(source='link_deadline')
    is_expired = graphene.Boolean(source='is_expired')


class Query(object):
    secure_link = graphene.Field(SecureLinkType)
    all_secure_links = graphene.List(SecureLinkType)

    @login_required
    def resolve_all_secure_links(self, info, **kwargs):
        return SecureLink.objects.all()

    @login_required
    def resolve_secure_link(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return SecureLink.objects.get(pk=id)


class SecureLinkMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        file_id = graphene.ID()

    # The class attributes define the response of the mutation
    secure_link = graphene.Field(SecureLinkType)

    @login_required
    def mutate(self, info, file_id):
        # 0. Найти модели по входным ID
        _, id_ = from_global_id(file_id)
        file = File.objects.get(pk=id_)

        secure_link = SecureLink()

        # 1. связать юзера с моделью
        secure_link.user = info.context.user

        # 2. сгенерировать ссылку, связать с моделью
        domain_name = info.context.environ['HTTP_HOST']  # получить имя домена, с которого пользователь зашел
        secure_link.url = secure_link.generate_secure_link(file.filename, domain_name)
        secure_link.save()

        # 3. связать файл с моделью
        file.secure_link = secure_link
        file.save()

        # Notice we return an instance of this mutation
        return SecureLinkMutation(secure_link=secure_link)


class Mutation:
    create_secure_link = SecureLinkMutation.Field()
