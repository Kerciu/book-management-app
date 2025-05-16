from django.db import models
from book.models import Book
from authentication.models import CustomUser
# Create your models here.
class BookReviews(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    pk = models.CompositePrimaryKey("user_id", "book_id")

    review = models.TextField(null=False)