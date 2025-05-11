from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, db_index=True)

    bio = models.TextField(blank=True)

    birth_date = models.DateField(null=True, blank=True, db_index=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    website = models.URLField(blank=True, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author)

    genres = models.ManyToManyField(Genre)

    isbn = models.CharField(
        max_length=13, unique=True, validators=[MinLengthValidator(10)]
    )

    published_at = models.DateField(null=True, blank=True, db_index=True)
    publishers = models.ManyToManyField(Publisher)

    page_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=30, default="English")

    cover_image = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return self.title

    @classmethod
    def update_search_vector(cls):
        cls.objects.update(search_vector=SearchVector("title", "description"))
