from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Shelf

User = get_user_model()

# signal to create default shelves for user
@receiver(post_save, sender=User)
def create_default_shelves(sender, instance, created, **kwargs):
    if created:
        Shelf.objects.create(
            user=instance,
            shelf_type='want_to_read',
            is_default=True
        )
        Shelf.objects.create(
            user=instance,
            shelf_type='currently_reading',
            is_default=True
        )
        Shelf.objects.create(
            user=instance,
            shelf_type='read',
            is_default=True
        )
