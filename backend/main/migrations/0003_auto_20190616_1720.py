# Generated by Django 2.2.2 on 2019-06-16 12:20

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_file_is_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/opt/services/django_nginx_secure_link/media'), upload_to=''),
        ),
    ]
