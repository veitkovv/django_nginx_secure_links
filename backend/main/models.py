from django.db import models
from django.conf import settings


class File(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    path = models.FilePathField(verbose_name='Путь до файла', path=settings.SHARE_ROOT, max_length=255, unique=True,
                                editable=False)
    secure_link = models.URLField(verbose_name='Публичная ссылка', blank=True, null=True, editable=False)
