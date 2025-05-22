from django.test import TestCase
from rest_framework.serializers import ValidationError

from ...serializers import GenreSerializer
from ...models import Genre


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

    def test_duplicate_genre_name(self):
        Genre.objects.create(name="Fantasy")
        data = {"name": "Fantasy"}

        serializer = GenreSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("name", context.exception.detail)
        self.assertIn("already exists", str(context.exception))
