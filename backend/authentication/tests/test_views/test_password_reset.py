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

    @patch('authentication.utils.send_password_reset_email')
    @patch('authentication.utils.generate_password_reset_tokens')
    def test_successful_reset_request(self, mock_tokens, mock_email):
        mock_tokens.return_value = ('test-uid', 'test-email')

        response = self.client.post(self.url, { 'email': 'test@example.com' })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "If this email exists, a reset link has been sent")
        mock_email.assert_called_once()

    def test_nonexistent_email_response(self):
        response = self.client.post(self.url, { 'email': 'non existent email' })

        # even for nonexistent emails,
        # the view returns HTTP 200 with the same message
        # (to prevent email enumeration attacks)
        self.assertEqual(response.status_code, 200)
