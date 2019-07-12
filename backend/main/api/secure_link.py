# -*- coding: utf-8 -*-
import graphene
import logging
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_jwt.decorators import login_required

from ..filesystem import filesystem
from ..utils.common import get_link_deadline
from ..models import SecureLink

logger = logging.getLogger(__name__)


class SecureLinkNode(DjangoObjectType):
    class Meta:
        model = SecureLink
        interfaces = (graphene.relay.Node,)
        filter_fields = ['file_name', 'who_creates']

    link_deadline = graphene.DateTime(source='link_deadline')


class SecureLinkMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        filename = graphene.String()

    # The class attributes define the response of the mutation
    secure_link = graphene.String()  # Ссылка в формате nginx secure link
    link_deadline = graphene.DateTime()  # Время когда ссылка перестанет быть действительной для WEB API
    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, filename):
        logger.info(f'User "{info.context.user}" gonna be create secure link to file "{filename}"')
        domain_name = info.context.environ['HTTP_HOST']  # получить имя домена, с которого пользователь зашел
        secure_link = filesystem.generate_secure_link(domain_name, filename, info.context.user.profile.url_ttl)

        sl = SecureLink()
        sl.file_name = filename
        sl.secure_url = secure_link
        sl.who_creates = info.context.user
        sl.save()

        ok = True
        logger.info(f'User "{info.context.user}" successfully create secure link to file "{filename}"')
        return SecureLinkMutation(secure_link=secure_link, link_deadline=sl.link_deadline(), ok=ok)


class Query(object):
    link_deadline = graphene.DateTime(url=graphene.String())
    secure_link = graphene.relay.Node.Field(SecureLinkNode)
    all_secure_links = DjangoFilterConnectionField(SecureLinkNode)

    @login_required
    def resolve_link_deadline(self, info, url):
        try:
            return get_link_deadline(url)
        except Exception as e:
            logger.error(e)


class Mutation:
    create_secure_link = SecureLinkMutation.Field()
