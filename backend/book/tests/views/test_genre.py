from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from ...models import Genre


User = get_user_model()


class GenreViewSetTest(APITestCase):
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

        self.genre = Genre.objects.create(name="Fiction")

    def create_genre_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("genres-list")
        data = {"name": "Science Fiction"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_unique_name_validation(self):
        self.client.force_authenticate(self.admin)
        url = reverse("genres-list")
        data = {"name": "Fiction"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This genre already exists", str(response.data))

    def test_case_insensitive_name(self):
        self.client.force_authenticate(self.admin)
        url = reverse("genres-list")
        data = {"name": "FICTION"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_name(self):
        self.client.force_authenticate(self.admin)
        url = reverse("genres-detail", args=[self.genre.id])
        data = {"name": "Non-Fiction"}
        response = self.client.patch(url, data)
        self.genre.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.genre.name, "Non-Fiction")

    def test_delete_protection(self):
        from .models import Book

        book = Book.objects.create(title="Test Book", isbn="1234567890123")
        book.genres.add(self.genre)

        self.client.force_authenticate(self.admin)
        url = reverse("genres-detail", args=[self.genre.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
