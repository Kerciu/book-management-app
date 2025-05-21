from django.test import TestCase
from django.utils import timezone

from django.core.exceptions import ValidationError

from authentication.models import CustomUser
from book.models import Book, Author, Genre, Publisher

from ...models import Review, ReviewComment


class ReviewCommentModelTest(TestCase):
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

    def test_create_comment(self):
        comment = ReviewComment.objects.create(
            user=self.user, review=self.review, text="Great review!"
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.review, self.review)
        self.assertEqual(comment.text, "Great review!")
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)
        self.assertEqual(self.user.commented_reviews.count(), 1)
        self.assertEqual(self.review.comments.count(), 1)

    def test_text_required(self):
        comment = ReviewComment(user=self.user, review=self.review, text="")
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_ordering(self):
        now = timezone.now()
        comment1 = ReviewComment.objects.create(
            user=self.user, review=self.review, text="First comment"
        )
        ReviewComment.objects.filter(pk=comment1.pk).update(
            created_at=now - timezone.timedelta(hours=1)
        )

        comment2 = ReviewComment.objects.create(
            user=self.user, review=self.review, text="Second comment"
        )
        ReviewComment.objects.filter(pk=comment2.pk).update(created_at=now)

        comments = ReviewComment.objects.all()
        self.assertEqual(list(comments), [comment2, comment1])

    def test_str_representation(self):
        comment = ReviewComment.objects.create(
            user=self.user, review=self.review, text="Test comment"
        )
        expected_str = f"{self.user.username} commented on {self.review}"
        self.assertEqual(str(comment), expected_str)
