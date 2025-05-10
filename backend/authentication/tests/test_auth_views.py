from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import CustomUser, OneTimePassword


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-register")
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
            "re_password": "testpass123",
        }

    @patch("authentication.views.send_code_to_user")
    def test_successful_registration(self, mock_send_code):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="test@example.com").exists())
        mock_send_code.assert_called_once()

    def test_invalid_registration_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("authentication.views.send_code_to_user")
    def test_duplicate_email_registration(self, mock_send_code):
        CustomUser.objects.create_user(
            email="test@example.com", password="existingpass"
        )
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_send_code.assert_not_called()


class ValidateRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("validate-register")
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123", is_verified=False
        )
        self.otp = OneTimePassword.objects.create(user=self.user, code="123456")

    def test_successful_verification(self):
        response = self.client.post(self.url, {"otp": "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_invalid_otp(self):
        response = self.client.post(self.url, {"otp": "000000"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_verified_user(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.post(self.url, {"otp": "123456"})
        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)


class LoginUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("login")
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123", is_verified=True
        )
        self.factory = RequestFactory()

    @patch("django.contrib.auth.authenticate")
    def test_successful_login(self, mock_authenticate):
        mock_authenticate.return_value = self.user
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data["user"])

    def test_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrongpass"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unverified_user_login(self):
        CustomUser.objects.create_user(
            email="unverified@example.com", password="testpass123", is_verified=False
        )
        data = {"email": "unverified@example.com", "password": "testpass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ResendEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("resend-email")
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123", is_verified=False
        )

    @patch("authentication.views.send_code_to_user")
    def test_successful_resend(self, mock_send_code):
        response = self.client.post(self.url, {"email": "test@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_code.assert_called_once_with("test@example.com", resending=True)

    def test_nonexistent_email(self):
        response = self.client.post(self.url, {"email": "nonexistent@example.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("authentication.views.send_code_to_user")
    def test_old_otp_deleted(self, mock_send_code):
        OneTimePassword.objects.create(user=self.user, code="123456")
        self.client.post(self.url, {"email": "test@example.com"})
        self.assertEqual(OneTimePassword.objects.count(), 0)
        mock_send_code.assert_called_once()


class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123", first_name="Test"
        )
        self.url = reverse("password-reset")

    @patch("authentication.utils.send_password_reset_email")
    @patch("authentication.utils.generate_password_reset_tokens")
    def test_successful_reset_request(self, mock_tokens, mock_email):
        mock_tokens.return_value = ("test-uid", "test-email")

        response = self.client.post(self.url, {"email": "test@example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"], "If this email exists, a reset link has been sent"
        )
        mock_email.assert_called_once()

    def test_nonexistent_email_response(self):
        response = self.client.post(self.url, {"email": "non existent email"})

        # even for nonexistent emails,
        # the view returns HTTP 200 with the same message
        # (to prevent email enumeration attacks)
        self.assertEqual(response.status_code, 200)

    @patch("authentication.utils.send_password_reset_email")
    def test_email_sending_failure(self, mock_email):
        mock_email.side_effect = Exception("Email error")

        response = self.client.post(self.url, {"email": "test@example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"], "If this email exists, a reset link has been sent"
        )

    def test_missing_email_field(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)
