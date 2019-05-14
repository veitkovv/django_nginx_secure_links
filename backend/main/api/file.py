import graphene

from django.conf import settings
from django.contrib.auth import get_user_model

from ..base import FileList, FileObj, get_file_obj_by_id
from ..models import File as FileModel
from ..utils.nginx_secure_link import secure_link


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


class CreateSecureLink(graphene.Mutation):
    class Arguments:
        file_id = graphene.String()
        user_id = graphene.Int()

    ok = graphene.Boolean()
    file = graphene.Field(lambda: File)

    def mutate(self, info, file_id, user_id):
        # find FileObj by id
        file = get_file_obj_by_id(file_id)

        # creating model for secure link
        file_model = FileModel()
        file_model.path = file.file
        file_model.secure_link = secure_link(settings.SECURE_URL_ROOT + file.file)
        file_model.user = get_user_model().objects.get(id=user_id)
        file_model.save()

        # we should return a graphene object type
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

        ok = True
        return CreateSecureLink(file=file, ok=ok)


class Mutation(graphene.ObjectType):
    create_secure_link = CreateSecureLink.Field()
