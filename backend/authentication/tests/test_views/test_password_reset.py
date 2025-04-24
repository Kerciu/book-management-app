from django.test import TestCase
from ...models import CustomUser
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch

CustomUser = get_user_model()

class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test'
        )
        self.url = reverse('password-reset')

