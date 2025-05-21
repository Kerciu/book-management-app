from django.test import TestCase
from django.utils import timezone

from authentication.models import CustomUser
from book.models import Book, Author, Genre, Publisher


class ReviewLikeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="Testuser",
            email="test@email.com",
            first_name="test",
            last_name="user",
            password="test2137AA",
        )

        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author",
        )

        self.publisher = Publisher.objects.create(name="Test publisher")

        self.genre = Genre.objects.create(name="Test genre")

        book = Book.objects.create(
            title="Test Book",
            isbn="0987654321",
            published_at=timezone.now().date(),
            page_count=320,
            language="English",
        )

        book.authors.add(self.author)
        book.genres.add(self.genre)
        book.publishers.add(self.publisher)
