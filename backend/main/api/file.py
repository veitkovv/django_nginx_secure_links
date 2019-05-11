import graphene

from django.conf import settings

from ..base import FileList, FileObj


class File(graphene.ObjectType):
    """
    graphql representation of file object from base.py
    """
    id = graphene.ID()
    url = graphene.String()
    filename = graphene.String()
    extension = graphene.String()
    size = graphene.Int()
    modified = graphene.Float()
    file_type = graphene.String()
    is_folder = graphene.Boolean()
    has_url = graphene.Boolean()


class Query:
    file = graphene.Field(File, filename=graphene.String(required=True))

    def resolve_file(self, info, filename):
        file = FileObj(filename)

        result = File()
        result.id = file.get_graphql_id()
        result.url = file.get_file_url()
        result.filename = file.get_filename()
        result.extension = file.get_extension()
        result.size = file.get_size()
        result.modified = file.get_time()
        result.file_type = file.get_file_type()
        result.is_folder = file.is_folder()
        result.has_url = file.has_url()

        return result

    files = graphene.List(of_type=File)

    def resolve_files(self, info):
        result = []

        # File list object for walk through filesystem and collect
        # information about files with walk() method
        fl = FileList(path=settings.SECURE_LINK_PATH)
        fl.walk()

        # correlate 'files info' object with graphql representation of it
        for file in fl.file_list:
            f = File()  # new Graphql object
            f.id = file.get_graphql_id()
            f.url = file.get_file_url()
            f.filename = file.get_filename()
            f.extension = file.get_extension()
            f.size = file.get_size()
            f.modified = file.get_time()
            f.file_type = file.get_file_type()
            f.is_folder = file.is_folder()
            f.has_url = file.has_url()

            result.append(f)
        return result
