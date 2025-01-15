from rest_framework.generics import CreateAPIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from notifications.tasks import send_notifications


class NotificationCreateAPIView(CreateAPIView):
    """Создает уведомление и запускает задачу отправки пользователям."""

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        recipients = serializer.context.get("validated_recipients")

        # Разделяем получателей на email и telegram
        email_recipients = [
            recipient["value"]
            for recipient in recipients
            if recipient["type"] == "email"
        ]
        telegram_recipients = [
            recipient["value"]
            for recipient in recipients
            if recipient["type"] == "telegram"
        ]

        # Запуск задачи отправки уведомления в Celery
        send_notifications.apply_async(
            args=[
                notification.message,
                email_recipients,
                telegram_recipients,
                notification.id,
            ],
            eta=notification.scheduled_for,
        )
