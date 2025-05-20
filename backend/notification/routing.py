from django.urls import path
from .consumer import NotificationConsumer

websocket_urlpatters = [path("ws/notifications/", NotificationConsumer.as_asgi())]
