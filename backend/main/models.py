# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver

from .utils.common import get_link_deadline


class Profile(models.Model):
    """
    Extending current user model with 1-to-1 way
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    url_ttl = models.PositiveIntegerField(verbose_name='Время жизни ссылки', default=settings.DEFAULT_PUBLIC_URL_TTL,
                                          validators=[MinValueValidator(settings.MIN_PUBLIC_URL_TTL),
                                                      MaxValueValidator(settings.MAX_PUBLIC_URL_TTL)])


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SecureLink(models.Model):
    file_name = models.CharField(max_length=255, verbose_name='Имя файла', editable=False, db_index=True)
    secure_url = models.URLField(editable=False)
    who_creates = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Link: {self.file_name} - {self.create_time} by {self.who_creates.username}'

    def link_deadline(self):
        """Берет из строки (URL) число в конце (timestamp) и переводит в datetime"""
        return get_link_deadline(self.secure_url)
