import graphene

from django.conf import settings

from ..base import FileList, FileObj


class File(graphene.ObjectType):
    url = graphene.String()
    filename = graphene.String()
    extension = graphene.String()
    size = graphene.Int()
    modified = graphene.Float()
    is_folder = graphene.Boolean()


class Query:
    file = graphene.Field(File, filename=graphene.String(required=True))

    def resolve_file(self, info, filename):
        file = FileObj(filename)

        result = File()
        result.url = file.get_file_url()
        result.filename = file.get_filename()
        result.extension = file.get_extension()
        result.size = file.get_size()
        result.modified = file.get_time()
        result.is_folder = file.is_folder()

        return result

    file_list = graphene.List(of_type=File)

    def resolve_file_list(self, info):
        result = []

        fl = FileList(path=settings.SECURE_LINK_PATH)
        fl.walk()

        for file in fl.file_list:
            f = File()
            f.url = file.get_file_url()
            f.filename = file.get_filename()
            f.extension = file.get_extension()
            f.size = file.get_size()
            f.modified = file.get_time()
            f.is_folder = file.is_folder()

            result.append(f)
        return result
