from django.test import TestCase
from ...models import Genre


class GenreModelTest(TestCase):
    def test_str_method(self):
        genre = Genre.objects.create(name="Fantasy")
        self.assertEqual(str(genre), "Fantasy")
