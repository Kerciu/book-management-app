from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Shelf(models.Model):
    SHELF_TYPES = (
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('read', 'Read'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves")
    name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(5)]
    )
    is_default = models.BooleanField(default=False)
    shelf_type = models.CharField(max_length=20, choices=SHELF_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (by {self.user.username})"


