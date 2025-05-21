from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from django.core.exceptions import ValidationError

from authentication.models import CustomUser
from book.models import Book, Author, Genre, Publisher

from ...models import Review


class ReviewModelTest(TestCase):
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

        self.publisher = Publisher.objects.create(
            name="Test publisher", website="http://penguin.pl"
        )

        self.genre = Genre.objects.create(name="Test genre")

        self.book = Book.objects.create(
            title="Test Book",
            isbn="0987654321",
            published_at=timezone.now().date(),
            page_count=320,
            language="English",
        )

        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
        self.book.publishers.add(self.publisher)

    def test_create_review(self):
        review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            text="very nice book",
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, "very nice book")
        self.assertFalse(review.has_spoilers)
        self.assertTrue(review.is_public)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_unique_user_book_constraint(self):
        Review.objects.create(
            user=self.user, book=self.book, rating=4, text="Good book"
        )
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user, book=self.book, rating=3, text="Duplicate review"
            )

    def test_rating_validation(self):
        review = Review(user=self.user, book=self.book, rating=0)
        with self.assertRaises(ValidationError):
            review.full_clean()

        review = Review(user=self.user, book=self.book, rating=6)
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_text_field_blank(self):
        review = Review.objects.create(
            user=self.user, book=self.book, rating=3, text=""
        )
        self.assertEqual(review.text, "")

    def test_default_values(self):
        review = Review.objects.create(user=self.user, book=self.book, rating=4)
        self.assertFalse(review.has_spoilers)
        self.assertTrue(review.is_public)

    def test_str_representation(self):
        review = Review.objects.create(user=self.user, book=self.book, rating=5)
        expected_str = f"{self.user.username}'s review of {self.book.title}"
        self.assertEqual(str(review), expected_str)
