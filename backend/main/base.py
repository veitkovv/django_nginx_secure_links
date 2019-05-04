import os
import mimetypes
from .models import File

from django.conf import settings

EXTENSIONS = getattr(settings, "FILEBROWSER_EXTENSIONS", {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'Video': ['.mov', '.mp4', '.m4v', '.webm', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.wav', '.aiff', '.midi', '.m4p']
})


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

    @property
    def abs_path(self):
        return os.path.join(settings.SECURE_LINK_PATH, self.file)

    def __repr__(self):
        return f'File: {self.file}'

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

    def get_mimetype(self):
        mtype, encoding = mimetypes.guess_type(self.abs_path)
        return mtype

    def get_file_url(self):
        file_model = File.objects.filter(path=self.abs_path)
        return file_model.secure_link if file_model else ''
