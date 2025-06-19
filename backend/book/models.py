from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100) # we denormalize db 
    birth_date = models.DateField(null=True, blank=True, db_index=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name}"


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    website = models.URLField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField(Author)

    genres = models.ManyToManyField(Genre)

    isbn = models.CharField(max_length=17, unique=True)

    published_at = models.DateField(null=True, blank=True, db_index=True)
    publishers = models.ManyToManyField(Publisher)

    page_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=30, default="English")

    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
