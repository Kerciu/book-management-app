from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ValidationError as URLValidationError

from .serializers import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
)

from .models import Author, Genre, Publisher

# Create your tests here.


class AuthorSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1906-06-25",
            "death_date": "1950-01-21",
        }

    def test_valid_author(self):
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_death_date_before_birth(self):
        invalid_data = self.valid_data.copy()
        invalid_data["death_date"] = "1905-06-25"
        serializer = AuthorSerializer(data=invalid_data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Death date must be after birth date", str(context.exception))

    def test_valid_missing_fields(self):
        copied_data = self.valid_data.copy()

        del copied_data["birth_date"]
        del copied_data["death_date"]

        serializer = AuthorSerializer(data=copied_data)
        self.assertTrue(serializer.is_valid())


class PublisherSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Kacper Gorski Publisher",
            "website": "https://kerciu.github.io/",
            "description": "Real cool website, go check that out",
        }

        self.invalid_data = {
            "name": "Invalid publisher",
            "website": "not a url",
        }

    def test_valid_publisher(self):
        serializer = PublisherSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_publisher_website(self):
        serializer = PublisherSerializer(data=self.invalid_data)
        with self.assertRaises(URLValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Enter a valid URL", str(context.exception))


class GenreSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {"name": "Warsaw University of Technology"}
        self.invalid_data = {"name": ""}

    def test_valid_genre(self):
        serializer = GenreSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_genre_missing_required_name(self):
        serializer = GenreSerializer(data=self.invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("This field may not be blank.", str(context.exception))


class BookSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="J.R.R.", last_name="Tolkien")
        self.publisher = Publisher.objects.create(name="Houghton Mifflin")
        self.genre = Genre.objects.create(name="Fantasy")

        self.valid_data = {
            "title": "The Lord of the Rings",
            "isbn": "9780544003415",
            "published_at": "1954-07-29",
            "page_count": 1178,
            "language": "English",
            "authors_ids": [self.author.id],
            "genres_ids": [self.genre.id],
            "publishers_ids": [self.publisher.id],
        }

    def test_valid_book_creation(self):
        serializer = BookSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_future_publish_date(self):
        invalid_data = self.valid_data.copy()
        invalid_data["published_at"] = "2137-07-29"

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "Publication date cannot be in the future", str(context.exception)
        )

    def test_author_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data["authors_ids"] = []

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("At least one author is required", str(context.exception))

    def test_genre_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data["genres_ids"] = []

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("At least one genre is required", str(context.exception))

    def test_valid_isbn_creation(self):
        data = self.valid_data.copy()
        data["isbn"] = "0544003411"
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_isbn_with_non_digit_char(self):
        data = self.valid_data.copy()
        data["isbn"] = "978-05440A3415"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("ISBN must contain only digits", str(context.exception))

    def test_invalid_isbn_length(self):
        data = self.valid_data.copy()
        data["isbn"] = "12345"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("ISBN must be 10 or 13 digits long", str(context.exception))

    def test_invalid_isbn_checksum(self):
        data = self.valid_data.copy()
        data["isbn"] = "0000000000"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Invalid ISBN checksum", str(context.exception))


class BookViewSetTest(TestCase):
    pass


class AuthorViewSetTest(TestCase):
    pass


class PublisherViewSetTest(TestCase):
    pass


class GenreViewSetTest(TestCase):
    pass
