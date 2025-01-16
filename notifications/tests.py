from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notifications.models import Notification, NotificationLog
from notifications.serializers import NotificationSerializer
from notifications.services import send_email_message, send_telegram_message
from notifications.tasks import send_notifications


class NotificationTestCase(APITestCase):

    def test_notification_create(self):
        """Тест на успешное создание уведомления с валидными данными."""

        url = reverse("notifications:notify")
        data = {
            "message": "Test message",
            "recipients": ["test@example.com", "12345678"],
            "delay": 0,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.all().count(), 1)

    def test_notification_create_invalid_email(self):
        """Тест на создание уведомления с некорректным email."""

        url = reverse("notifications:notify")
        data = {
            "message": "Test message",
            "recipients": ["invalid_email", "12345678"],
            "delay": 0,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Некорректный получатель: invalid_email. Укажите email или Telegram ID.",
            response.json()["recipients"],
        )

    def test_notification_create_invalid_telegram_id(self):
        """Тест на создание уведомления с некорректным Telegram ID."""

        url = reverse("notifications:notify")
        data = {
            "message": "Test message",
            "recipients": ["test@example.com", "invalid_id"],
            "delay": 0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Некорректный получатель: invalid_id. Укажите email или Telegram ID.",
            response.json()["recipients"],
        )

    def test_serializer_with_string_recipients(self):
        """Тест обработки строки в поле recipients."""

        data = {
            "message": "Test message",
            "recipients": "test@example.com",
            "delay": 0,
        }
        serializer = NotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["recipients"], ["test@example.com"])

    def test_serializer_invalid_recipients(self):
        """Тестирует валидацию для недопустимого типа данных в поле recipients."""

        data = {"message": "Test message", "recipients": 123, "delay": 0}
        serializer = NotificationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["recipients"],
            "Получатели должны быть строкой или списком строк.",
        )


class SendEmailMessageTests(TestCase):
    def setUp(self):
        self.notification = Notification.objects.create(
            message="Test message", recipients=["test@example.com"], delay=0
        )

    @patch("notifications.services.send_mail")
    def test_send_email_message_success(self, mock_send_mail):
        """Тестирует успешную отправку email."""

        mock_send_mail.return_value = 1

        send_email_message(
            "Test message", self.notification.recipients, self.notification.pk
        )
        log = NotificationLog.objects.get(notification=self.notification.pk)

        self.assertTrue(log.is_success)
        self.assertEqual(log.server_response, "1")

    @patch("notifications.services.send_mail")
    def test_send_email_message_failure(self, mock_send_mail):
        """Тестирует ошибку при отправке email."""

        mock_send_mail.side_effect = Exception("SMTP error")

        send_email_message(
            "Test message", self.notification.recipients, self.notification.pk
        )
        log = NotificationLog.objects.get(notification=self.notification.pk)

        self.assertFalse(log.is_success)
        self.assertIn("Ошибка: SMTP error", log.server_response)


class SendTelegramMessageTests(TestCase):
    def setUp(self):
        self.notification = Notification.objects.create(
            message="Test message", recipients=["test@example.com"], delay=0
        )

    @patch("notifications.services.requests.get")
    def test_send_telegram_message_success(self, mock_get):
        """Тестирует успешную отправку уведомления в Telegram."""

        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_get.return_value = mock_response

        send_telegram_message(
            "Test message", self.notification.recipients, self.notification.pk
        )
        log = NotificationLog.objects.get(notification=self.notification.pk)

        self.assertTrue(log.is_success)
        self.assertEqual(log.server_response, "{'ok': True}")

    @patch("notifications.services.requests.get")
    def test_send_telegram_message_failure(self, mock_get):
        """Тестирует ошибку при отправке уведомления в Telegram."""

        mock_get.side_effect = Exception("Network error")

        send_telegram_message(
            "Test message", self.notification.recipients, self.notification.pk
        )
        log = NotificationLog.objects.get(notification=self.notification.pk)

        self.assertFalse(log.is_success)
        self.assertIn("Ошибка: Network error", log.server_response)


class SendNotificationsTaskTests(TestCase):

    @patch("notifications.tasks.send_email_message")
    @patch("notifications.tasks.send_telegram_message")
    def test_send_notifications(self, mock_send_telegram, mock_send_email):
        send_notifications("Test message", ["test@example.com"], ["123456"], 1)

        mock_send_email.assert_called_once_with("Test message", ["test@example.com"], 1)
        mock_send_telegram.assert_called_once_with("Test message", ["123456"], 1)
