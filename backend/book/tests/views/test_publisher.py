from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from ...models import Publisher


User = get_user_model()


class PublisherViewSetTest(APITestCase):
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

        self.publisher = Publisher.objects.create(
            name="Kacper Publisher", website="https://kerciu.github.io"
        )

    def test_create_publisher_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("publishers-list")
        data = {"name": "New Publisher", "website": "https://new.example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 2)

    def test_unique_name(self):
        self.client.force_authenticate(self.admin)
        url = reverse("publishers-list")
        data = {"name": "Kacper Publisher", "website": "https://different.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_website_validation(self):
        self.client.force_authenticate(self.admin)
        url = reverse("publishers-list")
        data = {"name": "Invalid Website", "website": "not-a-url"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_website(self):
        self.client.force_authenticate(self.admin)
        url = reverse("publishers-detail", args=[self.publisher.id])
        data = {"website": "https://updated.example.com"}
        response = self.client.patch(url, data)
        self.publisher.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.publisher.website, "https://updated.example.com")

    def test_empty_description(self):
        self.client.force_authenticate(self.admin)
        url = reverse("publishers-list")
        data = {"name": "No Description", "description": ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
