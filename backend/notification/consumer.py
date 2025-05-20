from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope["user"] == AnonymousUser:
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = f"notifications_{self.user.id}"

        await self.channel_layer.group_app(
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
