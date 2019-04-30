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

    @cached_property
    def is_folder(self):
        return os.path.isdir(self.path)

    @property
    def list_files(self):
        if self.is_folder:
            return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        return []

    def walk(self):
        for f in self.list_files:
            print(f)
