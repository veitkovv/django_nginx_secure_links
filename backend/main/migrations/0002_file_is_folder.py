# Generated by Django 2.2.1 on 2019-05-18 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_folder',
            field=models.BooleanField(default=False),
        ),
    ]
