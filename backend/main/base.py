import os
import base64

from .models import File

from django.conf import settings


class FileList:
    def __init__(self, path=None):
        self.path = path
        self.file_list = []

    def is_folder(self):
        return os.path.isdir(self.path)

    @property
    def _list_files(self):
        if self.is_folder:
            return [f for f in os.listdir(self.path)]
        return []

    def walk(self):
        for f in self._list_files:
            f_obj = FileObj(file=f)
            self.file_list.append(f_obj)


class FileObj:
    def __init__(self, file):
        self.file = file

    def __repr__(self):
        return f'File: {self.file}'

    def get_graphql_id(self):
        serialized_id = base64.b64encode(self.get_filename().encode()).decode()
        return serialized_id

    @property
    def abs_path(self):
        return os.path.join(settings.SECURE_LINK_PATH, self.file)

    def is_folder(self):
        return os.path.isdir(self.abs_path)

    def get_filename(self):
        _, filename = os.path.split(self.file)
        return filename

    def get_extension(self):
        _, ext = os.path.splitext(self.file)
        return ext

    def get_size(self):
        """File size in bytes"""
        statinfo = os.stat(self.abs_path)
        return statinfo.st_size

    def get_time(self):
        """linux modified time"""
        stat = os.stat(self.abs_path)
        return stat.st_mtime

    def get_file_url(self):
        file_model = File.objects.filter(path=self.abs_path)
        return file_model.secure_link if file_model else ''

    def url_expired(self):
        """TODO заглушка"""
        return False

    def get_file_type(self):
        """:return material icons names for frontend"""
        if self.is_folder():
            return 'folder'
        result = next((item for item in settings.EXTENSIONS.items() if self.get_extension() in item[1]), None)
        return result[0] if result else 'note'

    def has_url(self):
        if self.get_file_url() and not self.url_expired():
            return True
        return False
