from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


def send_activate_email_message(user_id):
    """
    Функция отправки письма с подтверждением для аккаунта
    """
    user = get_object_or_404(User, id=user_id)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('accounts:confirm_email', kwargs={'uidb64': uid, 'token': token})
    subject = f'Активируйте свой аккаунт, {user.username}!'
    message = render_to_string('email/confirmation.txt', {
        'user': user,
        'activation_url': f'http://{settings.ALLOWED_HOSTS[0]}{activation_url}',
    })
    return user.email_user(subject, message)


def send_contact_email_message(subject, email, content, ip, user_id):
    user = get_object_or_404(User, id=user_id) if user_id else None
    message = render_to_string('feedback/feedback_email_send.html', {
        'email': email,
        'content': content,
        'ip': ip,
        'user': user,
    })
    email = EmailMessage(subject, message, settings.EMAIL_SERVER, settings.EMAIL_ADMIN)
    email.send(fail_silently=False)
