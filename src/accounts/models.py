import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_place(instance, filename):
    # username_logo
    f_name = f'profile/ {instance.username}_logo'
    if os.path.exists(settings.MEDIA_ROOT / f_name):
        os.remove(settings.MEDIA_ROOT / f_name)
    return f_name


class User(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True)
    avatar = models.ImageField(upload_to=avatar_place, default='profile/default.png')
    birthday = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'user'

    def __str__(self):
        return self.username
