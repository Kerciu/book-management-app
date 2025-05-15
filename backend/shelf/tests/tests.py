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

    def test_custom_shelf_cannot_have_shelf_type(self):
        with self.assertRaises(ValidationError):
            Shelf.objects.create(user=self.user, name='Weird Shelf', shelf_type='read')

    def test_default_shelf_must_have_shelf_type(self):
        with self.assertRaises(ValidationError):
            Shelf.objects.create(user=self.user, name='Read', is_default=True)

    def test_unique_default_shelf_type_constraint(self):
        with self.assertRaises(Exception):
            Shelf.objects.create(user=self.user, is_default=True, shelf_type='read')

    def test_unique_shelf_name_per_user(self):
        Shelf.objects.create(user=self.user, name='To Reread')
        with self.assertRaises(Exception):
            Shelf.objects.create(user=self.user, name='To Reread')

    def test_different_users_can_have_same_custom_shelf_name(self):
        Shelf.objects.create(user=self.user, name='Classics')
        user2 = User.objects.create_user(
            username='bob',
            email='bob@gmail.com',
            first_name='Bob',
            last_name='Smith',
            password='safepwd')
        try:
            Shelf.objects.create(user=user2, name='Classics')  # Should not raise
        except Exception:
            self.fail('Should allow same shelf name for different users')

    def test_str_representation(self):
        shelf = Shelf.objects.get(user=self.user, shelf_type='read')
        self.assertEqual(str(shelf), f"Read (by {self.user.username})")
