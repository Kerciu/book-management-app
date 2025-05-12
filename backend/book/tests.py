from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ValidationError as URLValidationError

from .serializers import AuthorSerializer, PublisherSerializer

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
    pass


class BookSerializerTest(TestCase):
    pass


class BookViewSetTest(TestCase):
    pass


class AuthorViewSetTest(TestCase):
    pass


class PublisherViewSetTest(TestCase):
    pass


class GenreViewSetTest(TestCase):
    pass
