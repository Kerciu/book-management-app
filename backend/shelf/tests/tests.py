from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Shelf

User = get_user_model()


class ShelfModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice',
            email='alice@gmail.com',
            first_name='Alice',
            last_name='Smith',
            password='2137')

    def test_default_shelves_created_for_new_user(self):
        default_shelves = Shelf.objects.filter(user=self.user, is_default=True)
        self.assertEqual(default_shelves.count(), 3)
        shelf_names = default_shelves.values_list('name', flat=True)
        self.assertIn('Want to Read', shelf_names)
        self.assertIn('Currently Reading', shelf_names)
        self.assertIn('Read', shelf_names)
