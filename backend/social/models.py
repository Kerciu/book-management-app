from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F, Q, UniqueConstraint

User = get_user_model()


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_friend_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # cannot send more than one pending request from A → B
            UniqueConstraint(
                fields=["from_user", "to_user"],
                name="unique_friendship_request"
            ),
            # cannot send a request to yourself: from_user != to_user
            models.CheckConstraint(
                check=~Q(from_user=F('to_user')),
                name="no_self_friend_request"
            ),
        ]

    def clean(self):
        # disallow from_user == to_user
        if self.from_user == self.to_user:
            raise ValidationError("Cannot send a friend request to yourself.")

        # disallow if a Friendship already exists
        if Friendship.objects.filter(
            Q(user1=self.from_user, user2=self.to_user) |
            Q(user1=self.to_user, user2=self.from_user)
        ).exists():
            raise ValidationError("You are already friends with this user.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def accept(self):
        """
        - Create exactly one Friendship(user1, user2) with user1.pk < user2.pk
        - Delete this FriendshipRequest
        """
        first, second = sorted([self.from_user, self.to_user], key=lambda u: u.pk)
        Friendship.objects.create(user1=first, user2=second)
        self.delete()

    def reject(self):
        self.delete()

    def __str__(self):
        return f"Friend request: {self.from_user.username} → {self.to_user.username}"