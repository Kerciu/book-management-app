from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import NotificationService

from review.models import ReviewLike


@receiver(post_save, sender=ReviewLike)
def handle_review_like(sender, instance, created, **kwargs):
    if created:
        NotificationService.notify_review_liked(
            user=instance.user,
            review=instance.review,
        )
