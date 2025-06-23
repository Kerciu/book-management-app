from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from book.models import Book, Genre
from shelf.models import Shelf

User = get_user_model()


class UserStatisticsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            first_name="A",
            last_name="Lice",
            email="alice@example.com",
            password="pass123",
        )
        self.client = APIClient()
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.genre = Genre.objects.create(name="SF")
        self.book1 = Book.objects.create(
            title="Dune",
            isbn="1234567890123",
            language="English",
            page_count=412,
        )
        self.book2 = Book.objects.create(
            title="Hyperion",
            isbn="1234567890129",
            language="English",
            page_count=480,
        )
        self.book1.genres.add(self.genre)
        self.book2.genres.add(self.genre)

        self.want = Shelf.objects.get(user=self.user, shelf_type="want_to_read")
        self.current = Shelf.objects.get(user=self.user, shelf_type="currently_reading")
        self.read = Shelf.objects.get(user=self.user, shelf_type="read")

        self.stats_url = "/api/v1/users/me/stats/"

    def test_statistics_flow(self):
        """Dodajemy książki → sprawdzamy liczby → przenosimy na \"read\" → ponownie sprawdzamy."""

        self.want.books.add(self.book1)
        self.current.books.add(self.book2)

        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "read": 0,
                "in_progress": 1,
                "want_to_read": 1,
                "favourite_genre": None,
            },
        )

        self.want.books.remove(self.book1)
        self.current.books.remove(self.book2)
        self.read.books.add(self.book1, self.book2)

        response = self.client.get(self.stats_url)
        data = response.json()
        self.assertEqual(data["read"], 2)
        self.assertEqual(data["in_progress"], 0)
        self.assertEqual(data["want_to_read"], 0)
        self.assertEqual(data["favourite_genre"]["name"], "SF")




