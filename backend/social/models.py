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
        first, second = sorted([self.from_user, self.to_user], key=lambda u: u.pk)
        Friendship.objects.create(user1=first, user2=second)
        self.delete()

    def reject(self):
        self.delete()

    def __str__(self):
        return f"Friend request: {self.from_user.username} → {self.to_user.username}"


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_as_user1"
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_as_user2"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # enforce user1.pk < user2.pk so that each pair occurs only once
            models.CheckConstraint(
                check=Q(user1__lt=F('user2')),
                name="friendship_user1_lt_user2"
            ),
            # only one unique pair (user1, user2)
            UniqueConstraint(
                fields=["user1", "user2"],
                name="unique_friendship_pair"
            ),
        ]

    def __str__(self):
        return f"Friendship: {self.user1.username} ↔ {self.user2.username}"

    @classmethod
    def are_friends(cls, user1, user2) -> bool:
        first, second = sorted([user1, user2], key=lambda u: u.pk)
        return cls.objects.filter(user1=first, user2=second).exists()

    @classmethod
    def remove_friendship(cls, user1, user2):
        first, second = sorted([user1, user2], key=lambda u: u.pk)
        cls.objects.filter(user1=first, user2=second).delete()


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # cannot follow yourself: follower != followee
            models.CheckConstraint(
                check=~Q(follower=F('followee')),
                name="no_self_follow"
            ),
            # only one follow per (follower, followee)
            UniqueConstraint(
                fields=["follower", "followee"],
                name="unique_follow_pair"
            ),
        ]

    def clean(self):
        if self.follower == self.followee:
            raise ValidationError("Cannot follow yourself.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"