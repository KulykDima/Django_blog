from django.apps import AppConfig
from django.dispatch import Signal

from .utils import send_activation_notification

user_register = Signal()


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


def user_register_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_register.connect(user_register_dispatcher)
