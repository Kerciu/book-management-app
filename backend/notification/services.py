from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification


class NotificationService:
    @classmethod
    def send_notification(cls, user, notification_type, message, payload=None):

        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=message,
            payload=payload,
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user.id}",
            {
                "type": "notify",
                "notification_id": notification.id,
                "notification_type": notification_type,
                "message": message,
                "payload": payload,
                "timestamp": notification.created_at.isoformat(),
                "is_read": False,
            },
        )

        return notification
