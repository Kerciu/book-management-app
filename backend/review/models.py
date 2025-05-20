from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from ..book.models import Book

# Create your models here.

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_reviews"
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    text = models.TextField(blank=True, null=False)
    has_spoilers = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "book"]

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"


class ReviewLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_reviews"
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "review"]

    def __str__(self):
        return f"{self.user.username} liked {self.review}"


class ReviewComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commented_reviews"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} commented on {self.review}"
