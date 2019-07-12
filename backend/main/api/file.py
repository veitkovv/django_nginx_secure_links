# -*- coding: utf-8 -*-
import logging
import graphene
from graphql_jwt.decorators import login_required

from ..filesystem import filesystem
from ..models import SecureLink
from .secure_link import SecureLinkNode

logger = logging.getLogger(__name__)


class FileType(graphene.ObjectType):
    filename = graphene.String()
    exists = graphene.Boolean()
    size = graphene.String()
    modified = graphene.Float()
    is_folder = graphene.Boolean()
    tarball_created = graphene.Boolean()
    file_type = graphene.String()
    secure_links_created = graphene.List(SecureLinkNode)

    def resolve_filename(self, info):
        return self.filename

    def resolve_exists(self, info):
        return self.exists

    def resolve_size(self, info):
        return self.size

    def resolve_modified(self, info):
        return self.modified

    def resolve_is_folder(self, info):
        return self.is_folder

    def resolve_tarball_created(self, info):
        """Создан ли архив для папки"""
        return filesystem.is_file_exists(self.filename + '.tar') if self.is_folder else False

    def resolve_file_type(self, info):
        return self.get_file_type()

    def resolve_secure_links_created(self, info):
        return self.secure_links_created()


class Query(object):
    file = graphene.Field(FileType)
    all_files = graphene.List(FileType,
                              search_str=graphene.String(),
                              order_by=graphene.String(),
                              without_links_only=graphene.Boolean())

    @login_required
    def resolve_all_files(self, info, **kwargs):
        """
        :param: order_by: ab-asc, ab-desc, created-asc, created-desc;
        """
        all_files = filesystem.walk()  # rescan file system

        search = kwargs.get('search_str')
        order_by = kwargs.get('order_by')
        without_links_only = kwargs.get('without_links_only')

        if without_links_only:
            for f in all_files:
                if SecureLink.objects.filter(file_name__exact=f.filename):
                    all_files.remove(f)

        if search:
            all_files = [i for i in all_files if search.lower() in i.filename.lower()]
        if order_by == 'ab-asc':
            all_files.sort(key=lambda x: x.filename, reverse=False)
        elif order_by == 'ab-desc':
            all_files.sort(key=lambda x: x.filename, reverse=True)
        elif order_by == 'created-asc':
            all_files.sort(key=lambda x: x.modified, reverse=False)
        elif order_by == 'created-desc':
            all_files.sort(key=lambda x: x.modified, reverse=True)

        return all_files
