from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import NotificationService

from review.models import ReviewLike, ReviewComment


@receiver(post_save, sender=ReviewLike)
def handle_review_like(sender, instance, created, **kwargs):
    if created:
        NotificationService.notify_review_liked(
            user=instance.user,
            review=instance.review,
        )


@receiver(post_save, sender=ReviewComment)
def handle_review_comment(sender, instance, created, **kwargs):
    if created and instance.review.user != instance.user:
        NotificationService.notify_review_commented(
            user=instance.user,
            review=instance.review,
            comment=instance,
        )
