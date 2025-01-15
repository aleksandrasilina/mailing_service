import requests
from celery import shared_task
from django.core.mail import send_mail

from config import settings
from notifications.models import NotificationLog
from notifications.services import send_email_message, send_telegram_message


@shared_task
def send_notifications(
    message: str,
    email_recipients: list[str],
    telegram_recipients: list[str],
    notification_id: int,
):
    """Отправляет уведомления пользователям."""

    if email_recipients:
        send_email_message(message, email_recipients, notification_id)

    if telegram_recipients:
        send_telegram_message(message, telegram_recipients, notification_id)
