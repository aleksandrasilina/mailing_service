# Generated by Django 5.1.4 on 2025-01-15 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message",
                    models.CharField(
                        help_text="Введите текст сообщения",
                        max_length=1024,
                        verbose_name="Сообщение",
                    ),
                ),
                (
                    "recipients",
                    models.JSONField(
                        help_text="Укажите одного получателя или список получателей",
                        verbose_name="Получатель или список получателей",
                    ),
                ),
                (
                    "delay",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "без задержки"), (1, "1 час"), (2, "1 день")],
                        help_text="Выберите время задержки отправки уведомления",
                        verbose_name="Задержка отправки уведомления",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "scheduled_for",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время отправки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Уведомление",
                "verbose_name_plural": "Уведомления",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="NotificationLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipient", models.CharField(verbose_name="Получатель уведомления")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "is_success",
                    models.BooleanField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Статус уведомления",
                    ),
                ),
                (
                    "server_response",
                    models.TextField(
                        blank=True, null=True, verbose_name="Ответ сервера"
                    ),
                ),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="notifications.notification",
                        verbose_name="Уведомление",
                    ),
                ),
            ],
            options={
                "verbose_name": "Лог уведомления",
                "verbose_name_plural": "Логи уведомлений",
                "ordering": ["-created_at"],
            },
        ),
    ]
