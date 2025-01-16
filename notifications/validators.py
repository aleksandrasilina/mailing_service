import re

from rest_framework.exceptions import ValidationError


class RecipientsValidator:
    """Валидатор для проверки списка получателей (email или Telegram ID)."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Валидирует список получателей и возвращает список словарей с указанием типа (email или telegram) получателя.
        """

        validated_recipients = []

        for recipient in value:
            if re.match(r"(^[\w\.\+\-]+\@[\w]+\.[a-z]{2,}$)", recipient):
                validated_recipients.append({"type": "email", "value": recipient})
            elif re.match(r"^\d+$", recipient):
                validated_recipients.append({"type": "telegram", "value": recipient})
            else:
                raise ValidationError(
                    {
                        self.field: f"Некорректный получатель: {recipient}. Укажите email или Telegram ID."
                    }
                )

        return validated_recipients
