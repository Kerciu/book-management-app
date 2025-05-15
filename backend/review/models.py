from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from ..book.models import Book

# Create your models here.

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(
        MinValueValidator(1),
        MaxValueValidator(5),
    )


class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    average_rating = models.FloatField(
        MinValueValidator(1),
        MaxValueValidator(5),
    )

    num_reviews = models.PositiveIntegerField()
