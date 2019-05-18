# -*- coding: utf-8 -*-
import graphene
from graphene_django.types import DjangoObjectType

from ..models import File, FileSystem


class FileType(DjangoObjectType):
    class Meta:
        model = File
        interfaces = (graphene.relay.Node,)

    exists = graphene.Boolean(source='exists')
    size = graphene.Int(source='size')
    modified = graphene.Float(source='modified')
    file_type = graphene.String(source='get_file_type')


class Query(object):
    all_files = graphene.List(FileType)

    def resolve_all_files(self, info, **kwargs):
        fs = FileSystem()
        fs.walk()  # rescan file system
        return File.objects.all()
