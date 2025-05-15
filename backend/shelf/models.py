from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint

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
    shelf_type = models.CharField(
        max_length=20, choices=SHELF_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'shelf_type'],
                condition=Q(is_default=True),
                name='unique_deafult_shelf'
            ),
            UniqueConstraint(
                fields=['user', 'name'],
                name='unique_shelf_name_for_user'
            )
        ]

    def __str__(self):
        return f"{self.name} (by {self.user.username})"

    def clean(self):
        if self.is_default:
            if not self.shelf_type:
                raise ValidationError('Default shelves must have a shelf type')
            self.name = dict(self.SHELF_TYPES).get(self.shelf_type, self.name)
        else:
            if self.shelf_type:
                raise ValidationError('Custom shelves cannot have a shelf type')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise ValidationError('Default shelves cannot be deleted')
        super().delete(*args, **kwargs)
