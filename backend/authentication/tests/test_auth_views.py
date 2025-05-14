from unittest.mock import patch, ANY

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings
from django.core.cache import cache

from ..models import CustomUser


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("register")
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
        self.client.post(self.url, self.valid_data)
        mock_send_code.assert_called_once_with("test@example.com")

    def test_invalid_registration_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("authentication.views.send_code_to_user")
    def test_duplicate_email_registration(self, mock_send_code):
        CustomUser.objects.create_user(
            email="test@example.com",
            password="existingpass",
            username="existinguser",
            first_name="Existing",
            last_name="User",
        )
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_send_code.assert_not_called()


class ValidateRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("verify-user")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            is_verified=False,
        )

        cache.set(f"otp:{self.user.email}", "123456", timeout=300)

    def test_successful_verification(self):
        response = self.client.post(
            self.url, {"otp": "123456", "email": self.user.email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertIsNone(cache.get(f"otp:{self.user.email}"))

    def test_invalid_otp(self):
        response = self.client.post(self.url, {"otp": "000000"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_verified_user(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.post(
            self.url, {"otp": "123456", "email": self.user.email}
        )
        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)


class LoginUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("login")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            is_verified=True,
        )
        self.factory = RequestFactory()

    @patch("django.contrib.auth.authenticate")
    def test_successful_login(self, mock_authenticate):
        mock_authenticate.return_value = self.user
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["user"])

    def test_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrongpass"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unverified_user_login(self):
        CustomUser.objects.create_user(
            email="unverified@example.com",
            password="testpass123",
            username="unverified",
            first_name="Test",
            last_name="User",
            is_verified=False,
        )
        data = {"email": "unverified@example.com", "password": "testpass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ResendEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("resend-email")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            is_verified=False,
        )

    @patch("authentication.views.send_code_to_user")
    def test_successful_resend(self, mock_send_code):
        self.client.post(self.url, {"email": self.user.email})
        mock_send_code.assert_called_once_with(self.user.email, resending=True)

    def test_nonexistent_email(self):
        response = self.client.post(self.url, {"email": "nonexistent@example.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("authentication.utils.EmailMessage.send")
    def test_old_otp_deleted(self, mock_send):
        cache.set(f"otp:{self.user.email}", "123456", timeout=300)
        self.client.post(self.url, {"email": self.user.email})
        new_otp = cache.get(f"otp:{self.user.email}")
        self.assertNotEqual(new_otp, "123456")


class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.url = reverse("password-reset")

    @patch("authentication.views.send_password_reset_email")
    def test_successful_reset_request(self, mock_email):
        self.client.post(self.url, {"email": self.user.email})
        mock_email.assert_called_once_with(
            self.user, ANY, ANY, ANY  # uid  # token  # request
        )

    def test_nonexistent_email_response(self):
        response = self.client.post(self.url, {"email": "nonexistentemail@example.com"})

        # even for nonexistent emails,
        # the view returns HTTP 200 with the same message
        # (to prevent email enumeration attacks)
        self.assertEqual(response.status_code, 200)

    @patch("authentication.views.send_password_reset_email")
    def test_email_sending_failure(self, mock_email):
        mock_email.side_effect = Exception("Email error")

        response = self.client.post(self.url, {"email": self.user.email})

        self.assertEqual(response.status_code, 200)
        mock_email.assert_called_once()

    def test_missing_email_field(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)


class PasswordResetConfirmViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.url = reverse(
            "password-reset-confirm", kwargs={"uid": self.uid, "token": self.token}
        )

    def test_valid_reset_confirm(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

    def test_invalid_uid(self):
        invalid_url = reverse(
            "password-reset-confirm", kwargs={"uid": "invalid_uid", "token": self.token}
        )
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        invalid_url = reverse(
            "password-reset-confirm", kwargs={"uid": self.uid, "token": "invalid_token"}
        )
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("set-new-password")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="oldpassword",
            first_name="Test",
            last_name="User",
            is_verified=True,
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.valid_data = {
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "uid": self.uid,
            "token": self.token,
        }

    def test_successful_password_reset(self):
        response = self.client.patch(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_invalid_token(self):
        invalid_data = self.valid_data.copy()
        invalid_data["token"] = "invalid_token"
        response = self.client.patch(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("logout")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        refresh = RefreshToken.for_user(self.user)
        self.valid_data = {"refresh_token": str(refresh)}

    def test_successful_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        with self.assertRaises(TokenError):
            RefreshToken(self.valid_data["refresh_token"]).verify()

    def test_unauthenticated_logout(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GoogleSignInViewTest(TestCase):
    @patch("authentication.providers.GoogleAuth.validate")
    def test_successful_google_auth(self, mock_validate):
        mock_validate.return_value = {
            "aud": settings.GOOGLE_CLIENT_ID,
            "email": "google@example.com",
            "given_name": "Test",
            "family_name": "User",
            "sub": "google-user-id",
        }
        self.client = APIClient()
        url = reverse("google-auth")
        response = self.client.post(url, {"access_token": "valid_token"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    @patch("authentication.providers.GoogleAuth.validate")
    def test_invalid_google_token(self, mock_validate):
        mock_validate.return_value = None
        url = reverse("google-auth")
        response = self.client.post(url, {"access_token": "invalid_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GithubSignInViewTest(TestCase):
    @patch("authentication.providers.GithubAuth.retrieve_user_info")
    @patch("authentication.providers.GithubAuth.exchange_code_for_token")
    def test_successful_github_auth(self, mock_exchange, mock_retrieve):
        mock_exchange.return_value = "valid_token"
        mock_retrieve.return_value = {
            "login": "githubuser",
            "email": "github@example.com",
            "name": "GitHub User",
        }
        url = reverse("github-auth")
        response = self.client.post(url, {"code": "valid_code"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    @patch("authentication.providers.GithubAuth.exchange_code_for_token")
    def test_invalid_github_code(self, mock_exchange):
        mock_exchange.return_value = None
        url = reverse("github-auth")
        response = self.client.post(url, {"code": "invalid_code"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
