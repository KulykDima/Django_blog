import os
import uuid

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


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=1000)
    is_readed = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_readed', '-created']


class Feedback(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Letter_theme')
    email = models.EmailField(max_length=100, verbose_name='Email')
    content = models.TextField(max_length=500)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Date_of_create')
    ip_address = models.GenericIPAddressField(verbose_name='sender_IP', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'You have a letter from {self.email}'
