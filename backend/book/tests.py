from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ValidationError as URLValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from .serializers import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
)

from .models import Book, Author, Genre, Publisher

# Create your tests here.


class AuthorSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1906-06-25",
            "death_date": "1950-01-21",
        }

    def test_valid_author(self):
        serializer = AuthorSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_death_date_before_birth(self):
        invalid_data = self.valid_data.copy()
        invalid_data["death_date"] = "1905-06-25"
        serializer = AuthorSerializer(data=invalid_data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Death date must be after birth date", str(context.exception))

    def test_valid_missing_fields(self):
        copied_data = self.valid_data.copy()

        del copied_data["birth_date"]
        del copied_data["death_date"]

        serializer = AuthorSerializer(data=copied_data)
        self.assertTrue(serializer.is_valid())


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


class GenreSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {"name": "Warsaw University of Technology"}
        self.invalid_data = {"name": ""}

    def test_valid_genre(self):
        serializer = GenreSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_genre_missing_required_name(self):
        serializer = GenreSerializer(data=self.invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("This field may not be blank.", str(context.exception))

    def test_duplicate_genre_name(self):
        Genre.objects.create(name="Fantasy")
        data = {"name": "Fantasy"}

        serializer = GenreSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("name", context.exception.detail)
        self.assertIn("already exists", str(context.exception))


class BookSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="J.R.R.", last_name="Tolkien")
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
        data["created_at"] = "2020-01-01T00:00:00Z"
        data["updated_at"] = "2020-01-01T00:00:00Z"

        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()

        self.assertIsNotNone(book.created_at)
        self.assertIsNotNone(book.updated_at)
        self.assertNotEqual(book.created_at.isoformat(), "2020-01-01T00:00:00Z")

    def test_invalid_author_id(self):
        data = self.valid_data.copy()
        data["authors_ids"] = [99999]

        serializer = BookSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Invalid pk", str(context.exception))

    def test_multiple_authors(self):
        author2 = Author.objects.create(first_name="Christopher", last_name="Tolkien")
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


User = get_user_model()


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "Kacper",
            "Gorski",
            "password2137",
        )

        self.user = User.objects.create_superuser(
            "user",
            "user@example.com",
            "Kacper",
            "NotGorski",
            "password2137",
        )

        self.author1 = Author.objects.create(first_name="John", last_name="Doe")
        self.author2 = Author.objects.create(first_name="Jane", last_name="Smith")
        self.genre1 = Genre.objects.create(name="Fiction")
        self.genre2 = Genre.objects.create(name="Science Fiction")
        self.publisher1 = Publisher.objects.create(name="Test Publisher")
        self.publisher2 = Publisher.objects.create(name="Another Publisher")

        self.book1 = Book.objects.create(
            title="Test Book",
            isbn="1234567890123",
            language="English",
            page_count=300,
            published_at=timezone.now().date() - timezone.timedelta(days=365),
        )
        self.book1.authors.add(self.author1)
        self.book1.genres.add(self.genre1)
        self.book1.publishers.add(self.publisher1)

        self.book2 = Book.objects.create(
            title="Another Book",
            isbn="1234567890456",
            language="Spanish",
            page_count=150,
            published_at=timezone.now().date() - timezone.timedelta(days=100),
        )
        self.book2.authors.add(self.author2)
        self.book2.genres.add(self.genre2)
        self.book2.publishers.add(self.publisher2)

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_book(self):
        url = reverse("book-retrieve", args=[self.book1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["title"]), "Test Book")

    def test_filter_books_by_min_pages(self):
        url = reverse("book-list")
        response = self.client.get(url, {"min_pages": 200})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book1.id)

    def test_filter_books_by_max_pages(self):
        url = reverse("book-list")
        response = self.client.get(url, {"max_pages": 200})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_filter_books_by_language(self):
        url = reverse("book-list")
        response = self.client.get(url, {"language": "Spanish"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_filter_books_by_published_date_range(self):
        url = reverse("book-list")
        params = {
            "published_after": (timezone.now() - timezone.timedelta(days=200))
            .date()
            .isoformat(),
            "published_before": (timezone.now() - timezone.timedelta(days=50))
            .date()
            .isoformat(),
        }
        response = self.client.get(url, params)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_search_by_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Another"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_search_by_author_last_name(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Smith"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_default_ordering(self):
        url = reverse("book-list")
        response = self.client.get(url)
        titles = [item["title"] for item in response.data["results"]]
        self.assertEqual(titles, ["Another Book", "Test Book"])

    def test_custom_ordering(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-published_at"})
        dates = [item["published_at"] for item in response.data["results"]]
        self.assertTrue(dates[0] > dates[1])

    def test_pagination(self):
        for i in range(15):
            Book.objects.create(
                title=f"Book {i}",
                isbn=f"1234567890{i:03}",
                language="English",
                page_count=100,
            )

        url = reverse("book-list")
        response = self.client.get(url, {"page_size": 10})
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("?page=2", response.data["next"])

    # create(), retrieve(), update(), partial_update(), destroy() and list() actions.

    def test_create_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "isbn": "1234567890789",
            "authors_ids": [self.author1.id],
            "genres_ids": [self.genre1.id],
            "publishers_ids": [self.publisher1.id],
            "language": "French",
            "page_count": 200,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("book-list")
        data = {"title": "New Book", "isbn": "1234567890789"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-detail", args=[self.book1.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_partial_update_book_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("book-detail", args=[self.book1.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_destroy_book_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_isbn_creation(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-list")
        data = {
            "title": "Invalid Book",
            "isbn": "invalid-isbn",
            "authors_ids": [self.author1.id],
            "genres_ids": [self.genre1.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("isbn", response.data)

    def test_future_publish_date_creation(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-detail", args=[self.book1.id])
        future_date = (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
        response = self.client.patch(url, {"published_at": future_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_relationship(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-detail", args=[self.book1.id])
        data = {
            "authors_ids": [self.author1.id, self.author2.id],
            "genres_ids": [self.genre2.id],
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.authors.count(), 2)
        self.assertEqual(self.book1.genres.count(), 1)

    def test_empty_page_count(self):
        self.client.force_authenticate(self.admin)
        url = reverse("book-list")
        data = {
            "title": "No Pages Book",
            "isbn": "1234567890999",
            "authors_ids": [self.author1.id],
            "genres_ids": [self.genre1.id],
            "page_count": None,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["page_count"])


class AuthorViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "Kacper",
            "Gorski",
            "password2137",
        )

        self.user = User.objects.create_superuser(
            "user",
            "user@example.com",
            "Kacper",
            "NotGorski",
            "password2137",
        )

        self.author = Author.objects.create(
            first_name="Sigmund",
            last_name="Freud",
            birth_date="1900-01-01",
            death_date="1950-01-01",
        )

    def test_create_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-list")
        data = {
            "first_name": "Ernest",
            "last_name": "Hemingway",
            "birth_date": "1899-07-21",
            "death_date": "1961-07-02",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        url = reverse("author-detail", args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["last_name"], "Doe")

    def test_update_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-detail", args=[self.author.id])
        data = {"middle_name": "Edgar"}
        response = self.client.patch(url, data)
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.author.middle_name, "Edgar")

    def test_delete_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-detail", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("author-list")
        data = {"first_name": "New", "last_name": "Author"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("author-list")
        data = {"first_name": "Updated", "last_name": "Author"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("author-list", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_dates(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-list")
        data = {
            "first_name": "Invalid",
            "last_name": "Dates",
            "birth_date": "2000-01-01",
            "death_date": "1999-01-01",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Death date must be after birth date", str(response.data))

    def test_future_dates(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-detail", args=[self.author.id])
        future_date = (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
        response = self.client.patch(url, {"birth_date": future_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_optional_fields(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-list")
        data = {"first_name": "Fyodor", "last_name": "Dostoevsky"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["death_date"])

    def test_max_length_fields(self):
        self.client.force_authenticate(self.admin)
        url = reverse("author-list")
        data = {
            "first_name": "A" * 101,
            "last_name": "Doe",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PublisherViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "Kacper",
            "Gorski",
            "password2137",
        )

        self.user = User.objects.create_superuser(
            "user",
            "user@example.com",
            "Kacper",
            "NotGorski",
            "password2137",
        )

        self.publisher = Publisher.objects.create(
            name="Kacper Publisher", website="https://kerciu.github.io"
        )

    def test_create_publisher_admin(self):
        pass

    def test_unique_name(self):
        pass

    def test_website_validation(self):
        pass

    def test_update_website(self):
        pass

    def test_empty_description(self):
        pass


class GenreViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "Kacper",
            "Gorski",
            "password2137",
        )

        self.user = User.objects.create_superuser(
            "user",
            "user@example.com",
            "Kacper",
            "NotGorski",
            "password2137",
        )

        self.genre = Genre.objects.create(name="Fiction")

    def create_genre_admin(self):
        pass

    def test_unique_name_validation(self):
        pass

    def test_case_insensitive_name(self):
        pass

    def test_update_name(self):
        pass

    def test_delete_protection(self):
        pass
