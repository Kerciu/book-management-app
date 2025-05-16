from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from book.models import Book
from authentication.models import CustomUser
# Create your models here.

class Rating:
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pk = models.CompositePrimaryKey("user_id", "book_id")
    rating = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1), MaxValueValidator(5)
        ])