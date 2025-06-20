from django.test import TestCase
from rest_framework.serializers import ValidationError

from ...serializers import BookSerializer
from ...models import Book, Author, Genre, Publisher


class BookSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        self.publisher = Publisher.objects.create(name="Houghton Mifflin")
        self.genre = Genre.objects.create(name="Fantasy")

        self.valid_data = {
            "title": "The Lord of the Rings",
            "isbn": "9780544003415",
            "published_at": "1954-07-29",
            "page_count": 1178,
            "language": "English",
            "authors_ids": [self.author.id],
            "genres_ids": [self.genre.id],
            "publishers_ids": [self.publisher.id],
        }

    def test_valid_book_creation(self):
        serializer = BookSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_future_publish_date(self):
        invalid_data = self.valid_data.copy()
        invalid_data["published_at"] = "2137-07-29"

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "Publication date cannot be in the future", str(context.exception)
        )

    def test_author_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data["authors_ids"] = []

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("At least one author is required", str(context.exception))

    def test_genre_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data["genres_ids"] = []

        serializer = BookSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("At least one genre is required", str(context.exception))

    def test_valid_isbn_creation(self):
        data = self.valid_data.copy()
        data["isbn"] = "0544003411"
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_isbn_with_non_digit_char(self):
        data = self.valid_data.copy()
        data["isbn"] = "978-05440A3415"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("ISBN must contain only digits", str(context.exception))

    def test_invalid_isbn_length(self):
        data = self.valid_data.copy()
        data["isbn"] = "12345"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("ISBN must be 10 or 13 digits long", str(context.exception))

    def test_invalid_isbn_checksum(self):
        data = self.valid_data.copy()
        data["isbn"] = "0000000000"
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Invalid ISBN checksum", str(context.exception))

    def test_partial_update(self):
        book = Book.objects.create(
            title="Original Title", isbn="9780544003415", published_at="2020-01-01"
        )
        book.authors.add(self.author)
        book.genres.add(self.genre)

        update_data = {"title": "Updated Title", "page_count": 1000}

        serializer = BookSerializer(instance=book, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_book = serializer.save()

        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.page_count, 1000)

        # verifying existing relationships preserved
        self.assertEqual(updated_book.authors.count(), 1)

    def test_partial_update_invalid(self):
        book = Book.objects.create(
            title="Original Title", isbn="9780544003415", published_at="2020-01-01"
        )
        book.authors.add(self.author)

        update_data = {"authors_ids": []}

        serializer = BookSerializer(instance=book, data=update_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("At least one author is required", str(context.exception))

    def test_title_length_validation(self):
        data = self.valid_data.copy()
        data["title"] = "A" * 256
        serializer = BookSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "Ensure this field has no more than 255 characters", str(context.exception)
        )

    def test_isbn_length_after_clean(self):
        data = self.valid_data.copy()
        data["isbn"] = "978-0-545-01022-1"
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_page_count_validation(self):
        data = self.valid_data.copy()
        data["page_count"] = 0
        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Page count must be at least 1", str(context.exception))

    def test_null_page_count(self):
        data = self.valid_data.copy()
        data["page_count"] = None
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_language_default(self):
        data = self.valid_data.copy()
        del data["language"]
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.language, "English")

    def test_read_only_fields(self):
        data = self.valid_data.copy()
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()

    def test_invalid_author_id(self):
        data = self.valid_data.copy()
        data["authors_ids"] = [99999]

        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Invalid pk", str(context.exception))

    def test_multiple_authors(self):
        author2 = Author.objects.create(name="Christopher Tolkien")
        data = self.valid_data.copy()
        data["authors_ids"] = [self.author.id, author2.id]

        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.authors.count(), 2)

    def test_duplicate_isbn(self):
        Book.objects.create(
            title="Existing Book", isbn="9780544003415", published_at="2020-01-01"
        )

        serializer = BookSerializer(data=self.valid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("isbn", context.exception.detail)
        self.assertIn("already exists", str(context.exception))

    def test_isbn_cleaning(self):
        data = self.valid_data.copy()
        data["isbn"] = "978-0-545-01022-1"

        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["isbn"], "9780545010221")
