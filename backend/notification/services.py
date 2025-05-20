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

    @classmethod
    def notify_review_liked(cls, user, review):
        message = f"{user.username} liked your review of {review.book.title}"
        return cls.send_notification(
            user=user,
            notification_type="REVIEW_LIKE",
            message=message,
            payload={
                "review_id": str(review.id),
                "book_id": str(review.book.id),
                "actor_id": str(user.id),
            },
        )

    @classmethod
    def notify_review_commented(cls, user, review, comment):
        message = f"{user.username} commented on your review of {review.book.title}"
        return cls.send_notification(
            user=user,
            notification_type="REVIEW_COMMENT",
            message=message,
            payload={
                "review_id": str(review.id),
                "comment_id": str(comment.id),
                "book_id": str(review.book.id),
                "actor_id": str(user.id),
            },
        )
