# -*- coding: utf-8 -*-
import os
import logging
import pytz
from datetime import datetime

from django.conf import settings

from .utils.nginx_secure_link import secure_link as make_link_secure
from .utils.common import sizeof_fmt
from .models import SecureLink

logger = logging.getLogger(__name__)


class FileSystem:
    """Класс для работы с файловой системой"""

    def __init__(self, path):
        self._path = path

    def walk(self):
        """
        Сканирование файловой системы по пути из settings.SECURE_LINK_PATH,
        возвращает генератор списка для дальнейшей работы в API
        """
        result = []
        logger.info(f'filesystem will be rescanned, path: {self._path}')
        try:
            # File objects with helper methods implemented below
            result = [File(f) for f in os.scandir(self._path) if f.name not in settings.FILTER_FILENAMES]
            logger.info(f'filesystem rescan complete: {[f.filename for f in result]}')
        except Exception as e:
            logger.info(e)

        return list(result)

    @staticmethod
    def generate_secure_link(domain_name, filename, ttl):
        secure_link = 'http://' + domain_name + '/secure/' + filename
        return make_link_secure(secure_link, ttl)

    def is_folder(self, filename):
        return os.path.isdir(os.path.join(self._path, filename))

    def is_file_exists(self, filename):
        return os.path.exists(os.path.join(self._path, filename))


class File:
    """Класс реализует методы для API"""

    def __init__(self, file):
        self.file = file

    def __str__(self):
        return f'FileObj: {self.file.name}'

    @property
    def filename(self):
        """
        Используется для генерации ссылки
        """
        return self.file.name

    @property
    def is_folder(self):
        return self.file.is_dir()

    @property
    def exists(self):
        return os.path.exists(self.file.path)

    def _get_folder_size(self):
        """Sum files sizes contains current folder"""
        return sum(os.path.getsize(f) for f in os.scandir(self.file.path) if os.path.isfile(f))

    @property
    def _raw_size(self):
        """
        :return: Возвращает размер файла или папки в байтах.
        """
        if self.exists:
            if self.is_folder:
                return self._get_folder_size()
            return os.path.getsize(self.file.path)
        return 0

    @property
    def size(self):
        return sizeof_fmt(self._raw_size)

    @property
    def modified(self):
        dt_created = datetime.fromtimestamp(int(self.file.stat().st_mtime))
        return dt_created.replace(tzinfo=pytz.UTC) if self.exists else None

    def get_file_type(self):
        """
        :return guessing file type
        """
        if self.is_folder:
            return 'folder'
        filename, ext = os.path.splitext(self.file.path)
        result = next((item for item in settings.EXTENSIONS.items() if ext in item[1]), None)
        return result[0] if result else 'undefined'

    def secure_links_created(self):
        return SecureLink.objects.filter(file_name__exact=self.filename)


filesystem = FileSystem(path=settings.SECURE_LINK_PATH)
