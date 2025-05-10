from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author)

    isbn = models.CharField(max_length=13, unique=True)
    published_at = models.DateField(null=True, blank=True)
    publishers = models.ManyToManyField(Publisher)

    page_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=30, default="English")

    cover_image = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
