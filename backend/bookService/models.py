from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateField(auto_now_add=True)
    password_hash = models.CharField(null=False)

    def __str__(self):
        return f"{self.username}"


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Authors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.name}"


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    published_at = models.DateField(null=False)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return f"{self.title}"


class BookCollections(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    books = models.ManyToManyField(Books)

    def __str__(self):
        return f"{self.name}"


class BookRatings(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    rating = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = [["user", "book"]]

    def __str__(self):
        return f"{self.user.username}'s rating for {self.book.title}"


class BookReviews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    review = models.TextField(null=False)

    class Meta:
        unique_together = [["user", "book"]]

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"


# TODO Users BookCollections relationship straightening out
# TODO Author Books relationship update in dbdiagram
#
