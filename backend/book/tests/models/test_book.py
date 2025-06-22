from django.test import TestCase
from django.utils import timezone
from ...models import Author, Publisher, Genre, Book


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.genre = Genre.objects.create(name="Science Fiction")
        self.publisher = Publisher.objects.create(
            name="SciPub", website="https://sci.pub"
        )

    def test_str_method(self):
        book = Book.objects.create(title="Django Deep Dive", isbn="1234567890")
        self.assertEqual(str(book), "Django Deep Dive")

    def test_create_book_with_relations(self):
        book = Book.objects.create(
            title="API Mastery",
            isbn="0987654321",
            published_at=timezone.now().date(),
            page_count=320,
            language="English",
        )
        book.authors.add(self.author)
        book.genres.add(self.genre)
        book.publishers.add(self.publisher)

        self.assertIn(self.author, book.authors.all())
        self.assertIn(self.genre, book.genres.all())
        self.assertIn(self.publisher, book.publishers.all())
