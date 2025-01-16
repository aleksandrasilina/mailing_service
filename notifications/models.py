from datetime import timedelta

from django.db import models
from django.utils.timezone import now

NULLABLE = {"blank": True, "null": True}
DELAY_MAPPING = {
    0: timedelta(),  # Без задержки
    1: timedelta(hours=1),  # 1 час
    2: timedelta(days=1),  # 1 день
}


class Notification(models.Model):
    DELAY_CHOICES = (
        (0, "без задержки"),
        (1, "1 час"),
        (2, "1 день"),
    )
    message = models.CharField(
        max_length=1024,
        verbose_name="Сообщение",
        help_text="Введите текст сообщения",
    )
    recipients = models.JSONField(
        verbose_name="Получатель или список получателей",
        help_text="Укажите одного получателя или список получателей",
    )
    delay = models.PositiveSmallIntegerField(
        choices=DELAY_CHOICES,
        verbose_name="Задержка отправки уведомления",
        help_text="Выберите время задержки отправки уведомления",
    )
    created_at = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    scheduled_for = models.DateTimeField(
        verbose_name="Время отправки",
        help_text="Время отправки с учетом задержки, заполняется автоматически",
        **NULLABLE,
    )

    def __str__(self):
        return f"Уведомление {self.message[:15] + '...' if len(self.message) > 15 else self.message}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Устанавливаем время отправки на основе задержки."""

        self.scheduled_for = now() + DELAY_MAPPING.get(self.delay, timedelta())
        super().save(*args, **kwargs)


class NotificationLog(models.Model):
    notification = models.ForeignKey(
        Notification,
        verbose_name="Уведомление",
        on_delete=models.CASCADE,
        related_name="logs",
    )
    recipient = models.CharField(
        max_length=150, verbose_name="Получатель уведомления", **NULLABLE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    is_success = models.BooleanField(
        verbose_name="Статус уведомления",
        editable=False,
        **NULLABLE,
    )
    server_response = models.TextField(verbose_name="Ответ сервера", **NULLABLE)

    def __str__(self):
        return f"Лог уведомления: {self.notification}"

    class Meta:
        verbose_name = "Лог уведомления"
        verbose_name_plural = "Логи уведомлений"
        ordering = ["-created_at"]
