from django.test import TestCase
from rest_framework.exceptions import ValidationError as URLValidationError

from ...serializers import PublisherSerializer


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
