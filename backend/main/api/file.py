import os
import json

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
    # file = graphene.relay.Node.Field(FileNode)
    # all_files = DjangoFilterConnectionField(FileNode)
    file_list = graphene.List(of_type=graphene.JSONString)

    def resolve_file_list(self, info):
        result = []
        fl = FileList(path=settings.SECURE_LINK_PATH)
        fl.walk()
        for item in fl.file_list:
            file_json = dict()
            file_json['is_folder'] = item.is_folder()
            file_json['filename'] = item.get_filename()
            file_json['extention'] = item.get_extension()
            file_json['modified'] = item.get_time()
            file_json['size'] = item.get_size()
            file_json['mimetype'] = item.get_mimetype()

            json.dumps(file_json)
            result.append(file_json)
        return result
