from django.db.models.signals import (
    post_save, post_delete, m2m_changed
)
from django.dispatch import receiver
from shelf.models import Shelf
from statistics.utils import recalculate_for
from django.conf import settings
from django.db.models.signals import post_save
from statistics.models import UserStatistics

@receiver([post_save, post_delete], sender=Shelf)
def shelf_changed(sender, instance, **kwargs):
    recalculate_for(instance.user)

@receiver(m2m_changed, sender=Shelf.books.through)
def shelf_books_changed(sender, instance, **kwargs):
    recalculate_for(instance.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="stats_autocreate")
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStatistics.objects.get_or_create(user=instance)