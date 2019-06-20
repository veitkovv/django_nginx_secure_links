# -*- coding: utf-8 -*-
import logging
import os

from django.db import models
from django.db.models import Q

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage

from .utils.nginx_secure_link import secure_link as make_link_secure

fs = FileSystemStorage(location=settings.SECURE_LINK_PATH)


class FileSystem(models.Model):
    class Meta:
        managed = False

    @property
    def secure_files_list(self):
        return fs.listdir(settings.SECURE_LINK_PATH)

    def walk(self):
        """
        discover new files and folders on filesystem
        :return: boolean
        """
        dirs, files = self.secure_files_list
        for file in files:
            obj, created = File.objects.filter(Q(file=file)).get_or_create(file=file)
            if created:
                logging.info(f'Файл "{obj}" синхронизирован')

        for folder in dirs:
            obj, created = File.objects.filter(Q(file=folder)).get_or_create(file=folder, defaults={'is_folder': True})
            if created:
                logging.info(f'Папка "{obj}" синхронизирована')


class File(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    file = models.FileField(storage=fs)
    file_discovered = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    secure_link = models.ForeignKey('SecureLink', blank=True, null=True, on_delete=models.CASCADE)
    is_folder = models.BooleanField(default=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def exists(self):
        return fs.exists(self.file.name)

    @property
    def size(self):
        return fs.size(self.file.name) if self.exists else 0

    @property
    def modified(self):
        return fs.get_modified_time(self.file.name).timestamp() if self.exists else None

    def get_file_type(self):
        """:return material icons names for frontend"""
        if self.is_folder:
            return 'folder'
        filename, ext = os.path.splitext(self.file.name)
        result = next((item for item in settings.EXTENSIONS.items() if ext in item[1]), None)
        return result[0] if result else 'note'


class SecureLink(models.Model):
    class Meta:
        verbose_name = 'Ссылка на файл'

    url = models.URLField(verbose_name='Публичная ссылка', editable=False)
    secure_link_created = models.DateTimeField(auto_now=True, verbose_name='Время создания ссылки', editable=False,
                                               null=True,
                                               blank=True)
    user = models.ForeignKey(get_user_model(), verbose_name='Кто создал ссылку', on_delete=models.DO_NOTHING,
                             blank=True, null=True)

    @staticmethod
    def generate_secure_link(filename):
        secure_link = 'http://' + settings.NGINX_SECURE_HOSTNAME + '/secure/' + filename
        return make_link_secure(secure_link)
