from django.test import TestCase
from rest_framework.serializers import ValidationError

from ...serializers import AuthorSerializer


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
