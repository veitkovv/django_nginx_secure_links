import os
import mimetypes
import time
import datetime

from django.conf import settings
from django.utils.functional import cached_property

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
            return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
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

    def is_folder(self):
        return os.path.isdir(self.file)

    def get_filename(self):
        _, filename = os.path.split(self.file)
        return filename

    def get_extension(self):
        _, ext = os.path.splitext(self.file)
        return ext

    def get_size(self):
        """File size in bytes"""
        statinfo = os.stat(os.path.join(settings.SECURE_LINK_PATH, self.file))
        return statinfo.st_size

    def get_time(self):
        """linux modified time"""
        stat = os.stat(os.path.join(settings.SECURE_LINK_PATH, self.file))
        return stat.st_mtime

    def get_mimetype(self):
        mtype, encoding = mimetypes.guess_type(os.path.join(settings.SECURE_LINK_PATH, self.file))
        return mtype
