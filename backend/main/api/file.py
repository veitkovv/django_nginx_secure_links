import os

import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.conf import settings

from ..models import File
from ..base import FileList


class FileNode(DjangoObjectType):
    class Meta:
        model = File
        interfaces = (graphene.relay.Node,)
        filter_fields = ['path', ]


class Query(object):
    file = graphene.relay.Node.Field(FileNode)
    all_files = DjangoFilterConnectionField(FileNode)
    file_list = graphene.List(of_type=graphene.String)

    def resolve_file_list(self, info):
        result = []
        fl = FileList(path=settings.MEDIA_ROOT)
        fl.walk()

        return result
