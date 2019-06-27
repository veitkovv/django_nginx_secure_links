# -*- coding: utf-8 -*-
import os
import tarfile
import logging

from django.conf import settings

from .utils.nginx_secure_link import secure_link as make_link_secure

logger = logging.getLogger(__name__)


class FileSystem:
    def __init__(self, path):
        self._path = path

    def walk(self):
        """
        discover new files and folders on filesystem
        """
        logger.info(f'filesystem will be rescanned, path: {self._path}')
        result = [File(f) for f in os.scandir(self._path)]
        logger.info(f'filesystem rescan complete: {[f.filename for f in result]}')
        return result

    def make_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    @staticmethod
    def generate_secure_link(domain_name, filename, ttl):
        secure_link = 'http://' + domain_name + '/secure/' + filename
        return make_link_secure(secure_link, ttl)


class File:
    def __init__(self, file):
        self.file = file

    def __str__(self):
        return f'FileObj: {self.file.name}'

    @property
    def filename(self):
        """
        Используется для генерации ссылки
        TODO генерировать ссылку на архив при создании ссылки на папку.
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
    def size(self):
        """
        :return: Возвращает размер файла или папки в байтах.
        """
        if self.exists:
            if self.is_folder:
                return self._get_folder_size()
            return os.path.getsize(self.file.path)
        return 0

    @property
    def modified(self):
        return self.file.stat().st_mtime if self.exists else None

    def get_file_type(self):
        """
        TODO move it to frontend
        :return material icons names for frontend
        """
        if self.is_folder:
            return 'folder'
        filename, ext = os.path.splitext(self.file.path)
        result = next((item for item in settings.EXTENSIONS.items() if ext in item[1]), None)
        return result[0] if result else 'note'


filesystem = FileSystem(path=settings.SECURE_LINK_PATH)
