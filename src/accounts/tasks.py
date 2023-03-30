from accounts.email import send_activate_email_message, send_contact_email_message

from celery import shared_task


@shared_task
def send_activate_email_message_task(user_id):
    """
    1. Задача обрабатывается в представлении: UserRegisterView
    2. Отправка письма подтверждения осуществляется через функцию: send_activate_email_message
    """
    return send_activate_email_message(user_id)


@shared_task
def send_feedback_email_message_task(subject, email, content, ip, user_id):
    "Реализация как в send_activate_email_message_task"
    return send_contact_email_message(subject, email, content, ip, user_id)
