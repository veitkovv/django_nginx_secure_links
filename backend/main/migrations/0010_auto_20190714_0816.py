# Generated by Django 2.2.3 on 2019-07-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_securelink_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securelink',
            name='file_name',
            field=models.CharField(db_index=True, editable=False, max_length=255, verbose_name='Имя файла'),
        ),
    ]