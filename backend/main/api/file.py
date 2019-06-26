# -*- coding: utf-8 -*-
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from ..models import File as FileModel
from ..utils import filesystem_helper as filesystem_utils


class FileType(DjangoObjectType):
    class Meta:
        model = FileModel
        interfaces = (graphene.relay.Node,)

    exists = graphene.Boolean(source='exists')
    size = graphene.Int(source='size')
    modified = graphene.Float(source='modified')
    file_type = graphene.String(source='get_file_type')
    min_ttl = graphene.Int(source='min_ttl')
    max_ttl = graphene.Int(source='max_ttl')
    filename = graphene.String(source='filename')


class Query(object):
    file = graphene.relay.Node.Field(FileType)
    all_files = graphene.List(FileType, search=graphene.String())

    @login_required
    def resolve_all_files(self, info, **kwargs):
        filesystem_utils.walk()  # rescan file system
        search = kwargs.get('search')
        queryset = FileModel.objects.filter(file__icontains=search)
        return queryset.order_by('file')
