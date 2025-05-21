from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Shelf

User = get_user_model()


class ShelfTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Jane',
            last_name='Doe',
            email='testuser@gmail.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.default_shelves = [
            Shelf.objects.create(
                user=self.user,
                name='Want to Read',
                shelf_type='want_to_read',
                is_default=True
            ),
            Shelf.objects.create(
                user=self.user,
                name='Currently Reading',
                shelf_type='currently_reading',
                is_default=True
            ),
            Shelf.objects.create(
                user=self.user,
                name='Read',
                shelf_type='read',
                is_default=True
            )
        ]

    def test_list_shelves(self):
        url = reverse('shelf-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # number of default shelves

    def test_create_shelf_valid(self):
        url = reverse('shelf-list')
        data = {
            'name': 'My Custom Shelf',
            'is_default': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shelf.objects.count(), 4)
        self.assertEqual(Shelf.objects.last().name, 'My Custom Shelf')

    def test_create_shelf_invalid_default(self):
        url = reverse('shelf-list')
        data = {
            'name': 'Invalid Default',
            'is_default': True,
            'shelf_type': 'want_to_read'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already exists')

    def test_retrieve_shelf(self):
        shelf = Shelf.objects.create(
            user=self.user,
            name='Test Shelf',
            is_default=False
        )
        url = reverse('shelf-detail', args=[shelf.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name', 'Test Shelf'])

    def test_update_shelf_valid(self):
        shelf = Shelf.objects.create(
            user=self.user,
            name='Original Name',
            is_default=False
        )
        url = reverse('shelf-detail', args=[shelf.id])
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shelf.refresh_from_db()
        self.assertEqual(shelf.name, 'Updated name')

    def test_update_default_shelf(self):
        default_shelf = self.default_shelves[0]
        url = reverse('shelf-detail', args=[default_shelf.id])
        data = {'name': 'New Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.asserIn('Cannot rename default shelves', str(response.data))

    def test_delete_shelf(self):
        shelf = Shelf.objects.create(
            user=self.user,
            name='To Delete',
            is_default=False
        )
        url = reverse('shelf-detail', args=[shelf.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Shelf.objects.count(), 3)

    def test_delete_default_shelf(self):
        default_shelf = self.default_shelves[0]
        url = reverse('shelf-detail', args=[default_shelf.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot delete default shelves', str(response.data))

    def test_unique_name_validation(self):
        Shelf.objects.create(
            user=self.user,
            name='Unique Shelf',
            is_default=False
        )

        url = reverse('shelf-list')
        data = {'name': 'Unique Shelf', 'is_default': False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already have a shelf', str(response.data))
        self.assertEqual(len(response.data), 4)

    def test_user_isolation(self):
        other_user = User.create_user(
            username='testuser2',
            first_name='Jane',
            last_name='Doe',
            email='testuser2@gmail.com',
            password='testpass123'
        )

        Shelf.objects.create(
            user=other_user,
            name='Other Shelf',
            is_default=False
        )

        response = self.client.get(reverse('shelf-list'))
        self.assertEqual(len(response.data), 3)