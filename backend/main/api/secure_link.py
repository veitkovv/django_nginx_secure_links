# -*- coding: utf-8 -*-
import graphene
import logging

from graphql_jwt.decorators import login_required

from ..filesystem import filesystem
from ..utils.common import get_link_deadline

logger = logging.getLogger(__name__)


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

        # Берет timestamp из URL посредством простой регулярки и сравнивает с текущим временем
        link_deadline = get_link_deadline(secure_link)

        ok = True
        logger.info(f'User "{info.context.user}" successfully create secure link to file "{filename}"')
        return SecureLinkMutation(secure_link=secure_link, link_deadline=link_deadline, ok=ok)


class Query(object):
    link_deadline = graphene.DateTime(url=graphene.String())

    @login_required
    def resolve_link_deadline(self, info, url):
        try:
            return get_link_deadline(url)
        except Exception as e:
            logger.error(e)


class Mutation:
    create_secure_link = SecureLinkMutation.Field()
