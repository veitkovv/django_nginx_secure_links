import os

import graphene
from ..models import File
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.conf import settings


class FileNode(DjangoObjectType):
    class Meta:
        model = File
        interfaces = (graphene.relay.Node,)
        filter_fields = ['path', ]


class Query(object):
    file = graphene.relay.Node.Field(FileNode)
    all_files = DjangoFilterConnectionField(FileNode)
    disk_files = graphene.List(of_type=graphene.String)

    def resolve_disk_files(self, info):
        result = []
        with os.scandir(settings.SHARE_ROOT) as dir_entries:
            for entry in dir_entries:
                if entry.is_file:
                    file_info = {}
                    info = entry.stat()
                    file_info['filename'] = entry.name
                    file_info['size'] = info.st_size
                    file_info['created_at'] = info.st_mtime
                    result.append(file_info)

        return result
