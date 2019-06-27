# -*- coding: utf-8 -*-
import re
import graphene
import logging

from datetime import datetime

from graphql_jwt.decorators import login_required

from ..filesystem import filesystem

logger = logging.getLogger(__name__)


class SecureLinkMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        filename = graphene.String()

    # The class attributes define the response of the mutation
    secure_link = graphene.String()  # Ссылка в формате nginx secure link
    link_deadline = graphene.DateTime()  # Время когда ссылка перестанет быть действительной для WEB API

    @login_required
    def mutate(self, info, filename):
        logger.info(f'User "{info.context.user}" gonna be create secure link to file {filename}')
        domain_name = info.context.environ['HTTP_HOST']  # получить имя домена, с которого пользователь зашел
        secure_link = filesystem.generate_secure_link(domain_name, filename, info.context.user.profile.url_ttl)

        # Берет timestamp из URL посредством простой регулярки и сравнивает с текущим временем
        link_deadline = datetime.fromtimestamp(int(re.search(r'[0-9]+$', str(secure_link)).group(0)))
        logger.info(f'User "{info.context.user}" successfully created secure link to file {filename}')
        return SecureLinkMutation(secure_link=secure_link, link_deadline=link_deadline)


class Mutation:
    create_secure_link = SecureLinkMutation.Field()
