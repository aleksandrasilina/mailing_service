from django.urls import path

from .apps import NotificationsConfig
from .views import NotificationCreateAPIView

app_name = NotificationsConfig.name

urlpatterns = [
    path("notify/", NotificationCreateAPIView.as_view(), name="notify"),
]
