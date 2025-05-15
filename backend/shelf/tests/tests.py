from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    def test_default_shelf_cannot_be_deleted(self):
        default_shelf = Shelf.objects.get(user=self.user, shelf_type='want_to_read')
        with self.assertRaises(ValidationError):
            default_shelf.delete()

    def test_default_shelf_name_is_forced_by_shelf_type(self):
        shelf = Shelf.objects.get(user=self.user, shelf_type='want_to_read')
        shelf.name = 'New Name'
        shelf.save()
        self.assertEqual(shelf.name, 'Want to Read')

    def test_custom_shelf_can_be_created_and_renamed_and_deleted(self):
        shelf = Shelf.objects.create(user=self.user, name='Favorites')
        shelf.name = 'Top Picks'
        shelf.save()
        self.assertEqual(shelf.name, 'Top Picks')
        shelf.delete()
        self.assertFalse(
            Shelf.objects.filter(user=self.user, name='Top Picks').exists())
