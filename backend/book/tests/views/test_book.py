from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from ...models import Book, Author, Genre, Publisher


User = get_user_model()


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            first_name="Kacper",
            last_name="Gorski",
            password="password2137",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            first_name="Kacper",
            last_name="NotGorski",
            password="password2137",
        )

        self.author1 = Author.objects.create(first_name="John", last_name="Doe")
        self.author2 = Author.objects.create(first_name="Jane", last_name="Smith")
        self.genre1 = Genre.objects.create(name="Fiction")
        self.genre2 = Genre.objects.create(name="Science Fiction")
        self.publisher1 = Publisher.objects.create(
            name="Test Publisher", website="http://first.com"
        )
        self.publisher2 = Publisher.objects.create(
            name="Another Publisher", website="http://first.com"
        )

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
        url = reverse("books")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_book(self):
        url = reverse("books", args=[self.book1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_filter_books_by_min_pages(self):
        url = reverse("books")
        response = self.client.get(url, {"min_pages": 200})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book1.id)

    def test_filter_books_by_max_pages(self):
        url = reverse("books")
        response = self.client.get(url, {"max_pages": 200})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_filter_books_by_language(self):
        url = reverse("books")
        response = self.client.get(url, {"language": "Spanish"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_filter_books_by_published_date_range(self):
        url = reverse("books")
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
        url = reverse("books")
        response = self.client.get(url, {"search": "Another"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_search_by_author_last_name(self):
        url = reverse("books")
        response = self.client.get(url, {"search": "Smith"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.book2.id)

    def test_default_ordering(self):
        url = reverse("books")
        response = self.client.get(url)
        titles = [item["title"] for item in response.data["results"]]
        self.assertEqual(titles, ["Another Book", "Test Book"])

    def test_custom_ordering(self):
        url = reverse("books")
        response = self.client.get(url, {"ordering": "-published_at"})
        dates = [item["published_at"] for item in response.data["results"]]
        self.assertTrue(dates[0] > dates[1])

    def test_pagination(self):
        for i in range(18):
            Book.objects.create(
                title=f"Book {i}",
                isbn=f"1234567890{i:03}",
                language="English",
                page_count=100,
            )

        url = reverse("books-list")
        response = self.client.get(url, {"page_size": 10})
        self.assertEqual(len(response.data["results"]), 10)

    # create(), retrieve(), update(), partial_update(), destroy() and list() actions.

    def test_create_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("books-list")
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
        url = reverse("books-list")
        data = {"title": "New Book", "isbn": "1234567890789"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("books", args=[self.book1.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_partial_update_book_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("books", args=[self.book1.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_book_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("books", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_destroy_book_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("books", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_isbn_creation(self):
        self.client.force_authenticate(self.admin)
        url = reverse("books")
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
        url = reverse("books", args=[self.book1.id])
        future_date = (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
        response = self.client.patch(url, {"published_at": future_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_relationship(self):
        self.client.force_authenticate(self.admin)
        url = reverse("books", args=[self.book1.id])
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
        url = reverse("books")
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
