from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves")

    name = models.CharField(min_length=5, max_length=30)
