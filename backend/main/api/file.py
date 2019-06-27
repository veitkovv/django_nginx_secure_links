# -*- coding: utf-8 -*-
import logging
import graphene
from graphql_jwt.decorators import login_required

from ..filesystem import filesystem

logger = logging.getLogger(__name__)


class FileType(graphene.ObjectType):
    filename = graphene.String()
    exists = graphene.Boolean()
    size = graphene.Int()
    modified = graphene.Float()
    is_folder = graphene.Boolean()
    file_type = graphene.String()

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

    def resolve_file_type(self, info):
        return self.get_file_type()


class Query(object):
    file = graphene.Field(FileType)
    all_files = graphene.List(FileType, search=graphene.String())

    @login_required
    def resolve_all_files(self, info, **kwargs):
        all_files = filesystem.walk()  # rescan file system
        search = kwargs.get('search')
        if search:
            return [i for i in all_files if search in i.filename]
        return all_files
