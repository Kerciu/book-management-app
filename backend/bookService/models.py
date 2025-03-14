from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False, default="")
    created_at = models.DateField(auto_now_add=True)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True, default="")

class Authors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)

class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    published_at = models.DateField(null=False)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categories)

class BookCollections(models.Model): 
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    book_id = models.ManyToManyField(Books)

class BookRatings(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    rating = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1), MaxValueValidator(5)
        ]
    )

class BookReviews(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    review = models.TextField(null=False)

