from django.conf import settings
from django.db import models
from book.models import Genre

class UserStatistics(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stats",
    )
    read = models.PositiveIntegerField(default=0)
    in_progress = models.PositiveIntegerField(default=0)
    want_to_read = models.PositiveIntegerField(default=0)
    favourite_genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Stats for {self.user}"