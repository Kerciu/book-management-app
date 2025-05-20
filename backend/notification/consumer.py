from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = f"notifications_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def notify(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def mark_as_read(self, notification_id):
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
