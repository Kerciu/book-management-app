from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ("REVIEW_LIKE", "Review Like"),
        ("REVIEW_COMMENT", "Review Comment"),
        ("COMMENT_REPLY", "Comment Reply"),
        ("FRIEND_ACTIVITY", "Friend Activity"),
        ("BOOK_RECOMMENDATION", "Book Recommendation"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notifications"
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    message = models.TimeField()
    payload = models.JSONField(default=dict)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read"])]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
