# -*- coding: utf-8 -*-
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from ..models import File, FileSystem


class FileType(DjangoObjectType):
    class Meta:
        model = File
        interfaces = (graphene.relay.Node,)

    exists = graphene.Boolean(source='exists')
    size = graphene.Int(source='size')
    modified = graphene.Float(source='modified')
    file_type = graphene.String(source='get_file_type')
    min_ttl = graphene.Int(source='min_ttl')
    max_ttl = graphene.Int(source='max_ttl')


class Query(object):
    all_files = graphene.List(FileType)

    @login_required
    def resolve_all_files(self, info, **kwargs):
        fs = FileSystem()
        fs.walk()  # rescan file system
        return File.objects.all()
