from django.test import TestCase
from django.core.exceptions import ValidationError
from ...serializers import PasswordResetRequestSerializer
from ...models import CustomUser
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
CustomUser = get_user_model()


class PasswordResetSerializerTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test'
        )
        self.url = reverse('password-reset')

    def test_valid_email(self):
        serializer = PasswordResetRequestSerializer(data={'email': 'test@example.com'})
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_email_format(self):
        serializer = PasswordResetRequestSerializer(data={'email': 'invalid-email'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_nonexistent_email(self):
        serializer = PasswordResetRequestSerializer(data={'email': 'nonexistent@example.com'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
