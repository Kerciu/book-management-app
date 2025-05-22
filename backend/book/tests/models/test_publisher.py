from django.test import TestCase
from ...models import Publisher


class PublisherModelTest(TestCase):
    def test_str_method(self):
        publisher = Publisher.objects.create(
            name="Tech Books", website="https://example.com"
        )
        self.assertEqual(str(publisher), "Tech Books")
