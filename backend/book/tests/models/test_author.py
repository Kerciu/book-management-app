from django.test import TestCase
from ...models import Author


class AuthorModelTest(TestCase):
    def test_str_method(self):
        author = Author.objects.create(name="John Doe")
        self.assertEqual(str(author), "John Doe")

    def test_optional_fields(self):
        author = Author.objects.create(
            name="Anna M. Smith"
        )
        self.assertIsNone(author.birth_date)
        self.assertIsNone(author.death_date)
