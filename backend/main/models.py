# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver



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

