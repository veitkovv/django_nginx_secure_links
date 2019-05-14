from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class File(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    path = models.FilePathField(verbose_name='Путь до файла', path=settings.SECURE_LINK_PATH, max_length=255,
                                unique=True,
                                editable=False)
    secure_link = models.URLField(verbose_name='Публичная ссылка', blank=True, null=True, editable=False)
    user = models.ForeignKey(get_user_model(), verbose_name='Кто создал ссылку', on_delete=models.DO_NOTHING,
                             blank=True, null=True)
    created = models.DateTimeField(auto_now=True, editable=False, verbose_name='Время создания ссылки')
