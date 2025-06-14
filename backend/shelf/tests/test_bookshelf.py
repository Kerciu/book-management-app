from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Shelf
from book.models import Book, Author, Genre, Publisher

User = get_user_model()


class ShelfBooksTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Jane',
            last_name='Doe',
            email='testuser@gmail.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.shelf = Shelf.objects.get(
            user=self.user, is_default=True, shelf_type='want_to_read')

        self.author = Author.objects.create(
            first_name="Anna",
            middle_name="M.",
            last_name="Smith"
        )
        self.genre = Genre.objects.create(name="Fantasy")
        self.publisher = Publisher.objects.create(
            name="Tech Books",
            website="https://example.com"
        )

        self.book = Book.objects.create(
            title="API Mastery",
            isbn="0987654321",
            published_at=timezone.now().date(),
            page_count=320,
            language="English",
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
        self.book.publishers.add(self.publisher)

    def test_add_book_to_shelf(self):
        url = reverse('shelf-add-book', args=[self.shelf.id])
        response = self.client.post(url, {"book_id": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.shelf.books.filter(id=self.book.id).exists())

    def test_add_duplicate_book_to_shelf_fails(self):
        self.shelf.books.add(self.book)
        url = reverse('shelf-add-book', args=[self.shelf.id])
        response = self.client.post(url, {"book_id": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0], "This book is already on the shelf.")

    def test_remove_book_from_shelf(self):
        self.shelf.books.add(self.book)
        self.shelf.refresh_from_db()
        url = reverse('shelf-remove-book', args=[self.shelf.id])
        response = self.client.post(url, {"book_id": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.shelf.books.filter(id=self.book.id).exists())

    def test_remove_book_not_in_shelf_fails(self):
        url = reverse('shelf-remove-book', args=[self.shelf.id])
        response = self.client.post(url, {"book_id": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Book not in shelf.")

    def test_add_nonexistent_book_fails(self):
        url = reverse('shelf-add-book', args=[self.shelf.id])
        response = self.client.post(url, {"book_id": 999999})  # non-existent ID
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book_id", response.data)

    def test_get_books_from_empty_shelf(self):
        url = reverse('shelf-books', args=[self.shelf.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
