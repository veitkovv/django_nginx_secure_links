import tarfile
import os
import logging

from django.db.models import Q
from django.conf import settings

from ..models import File as FileModel


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def walk():
    """
    discover new files and folders on filesystem, writing results to the model
    :return: boolean
    """
    for file in os.scandir(settings.SECURE_LINK_PATH):
        obj, created = FileModel.objects.filter(Q(file=file.name)).get_or_create(file=file.name,
                                                                                 defaults={'is_folder': file.is_dir()})
        if created:
            logging.info(f'Обнаружено: "{obj.name}"')
