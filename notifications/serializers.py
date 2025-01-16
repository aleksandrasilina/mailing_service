from rest_framework import serializers

from notifications.models import Notification
from notifications.validators import RecipientsValidator


class NotificationSerializer(serializers.ModelSerializer):
    recipients = serializers.ListField(
        child=serializers.CharField(max_length=150),
        write_only=True,
        help_text=(
            "Получатели уведомления (string(150) | list[string(150)])."
        ),
    )

    class Meta:
        model = Notification
        fields = "__all__"

    def to_internal_value(self, data):
        """Обрабатывает входные данные, валидирует получателей и сохраняет их в контексте."""

        # Создаем изменяемую копию данных
        data = data.copy()

        recipients = data.get("recipients")

        # Если передан один получатель как строка, преобразуем его в список
        if isinstance(recipients, str):
            data["recipients"] = [recipients]
        elif isinstance(recipients, list):
            data["recipients"] = recipients
        else:
            raise serializers.ValidationError(
                {"recipients": "Получатели должны быть строкой или списком строк."}
            )

        # Валидируем и сохраняем получателей с учетом их типа
        validated_recipients = RecipientsValidator(field="recipients")(
            data["recipients"]
        )
        self.context["validated_recipients"] = validated_recipients

        return super().to_internal_value(data)
