from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from ...models import Author


User = get_user_model()


class AuthorViewSetTest(APITestCase):
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

        self.author = Author.objects.create(
            name="Sigmund Freud",
            birth_date="1900-01-01",
            death_date="1950-01-01",
        )

    def test_create_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-list")
        data = {
            "name": "Ernest Hemingway",
            "birth_date": "1899-07-21",
            "death_date": "1961-07-02",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        url = reverse("authors-detail", args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Sigmund Freud")

    def test_update_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-detail", args=[self.author.id])
        data = {"name": "Edgar"}
        response = self.client.patch(url, data)
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.author.name, "Edgar")

    def test_delete_author_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-detail", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("authors-list")
        data = {"name": "New Author"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("authors-list")
        data = {"name": "Updated Author"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author_regular_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("authors-detail", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_dates(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-list")
        data = {
            "name": "Invalid Dates",
            "birth_date": "2000-01-01",
            "death_date": "1999-01-01",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Death date must be after birth date", str(response.data))

    def test_future_dates(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-detail", args=[self.author.id])
        future_date = (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
        response = self.client.patch(url, {"birth_date": future_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_optional_fields(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-list")
        data = {"name": "Fyodor Dostoevsky"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["death_date"])

    def test_max_length_fields(self):
        self.client.force_authenticate(self.admin)
        url = reverse("authors-list")
        data = {
            "name": "A" * 101 + "Doe",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
