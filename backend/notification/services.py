from .models import Notification


class NotificationService:
    @classmethod
    def send_notification(cls, user, notification_type, message, payload=None):

        _ = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=message,
            payload=payload,
        )
