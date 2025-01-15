import requests
from django.core.mail import send_mail

from config import settings
from notifications.models import NotificationLog


def send_email_message(message: str, email_recipients: list[str], notification_id: int):
    """Функция отправляет уведомления на почту и записывает логи в базу данных."""

    for email in email_recipients:
        log = NotificationLog.objects.create(
            notification_id=notification_id, recipient=email
        )
        try:
            server_response = send_mail(
                subject="Уведомление",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            log.server_response = server_response
            log.is_success = True
        except Exception as e:
            log.server_response = f"Ошибка: {e}"
            log.is_success = False
        finally:
            log.save()


def send_telegram_message(
    message: str, telegram_recipients: list[str], notification_id: int
):
    """Функция отправляет уведомления в Telegram и записывает логи в базу данных."""

    for chat_id in telegram_recipients:
        log = NotificationLog.objects.create(
            notification_id=notification_id, recipient=chat_id
        )
        try:
            params = {
                "chat_id": chat_id,
                "text": message,
            }

            response = requests.get(
                f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage",
                params=params,
            )

            log.server_response = response.json()
            log.is_success = True

        except Exception as e:
            log.server_response = f"Ошибка: {e}"
            log.is_success = False

        finally:
            log.save()
