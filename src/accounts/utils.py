from django.conf import settings
from django.core.signing import Signer
from django.template.loader import render_to_string

signer = Signer()


def send_activation_notification(user):
    if settings.ALLOWED_HOSTS:
        host = f'http://{settings.ALLOWED_HOSTS[0]}'
    else:
        host = 'http://localhost:12345'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body = render_to_string('email/activation_letter_body.txt', context)

    user.email_user(subject, body)


def get_client_ip(request):
    "Функция получения IP пользователя"
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip
