from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from authentication.models import CustomUser
from book.models import Book, Author, Genre, Publisher

from ...models import ReviewLike, Review


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

        self.review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            text="very nice book",
        )

    def test_create_like(self):
        like = ReviewLike.objects.create(user=self.user, review=self.review)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.review, self.review)
        self.assertIsNotNone(like.created_at)
        self.assertEqual(self.user.liked_reviews.count(), 1)
        self.assertEqual(self.review.likes.count(), 1)

    def test_unique_like_constraint(self):
        ReviewLike.objects.create(user=self.user, review=self.review)
        with self.assertRaises(IntegrityError):
            ReviewLike.objects.create(user=self.user, review=self.review)

    def test_str_representation(self):
        like = ReviewLike.objects.create(user=self.user, review=self.review)
        expected_str = f"{self.user.username} liked {self.review}"
        self.assertEqual(str(like), expected_str)
