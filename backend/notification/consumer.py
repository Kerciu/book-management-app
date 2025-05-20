from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def disconnect(self, code):
        return await super().disconnect(code)

    async def send_notification(self):
        return await self.send()
