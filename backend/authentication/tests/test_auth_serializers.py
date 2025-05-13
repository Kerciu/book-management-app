from unittest.mock import patch

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from ..models import CustomUser
from ..serializers import (
    GithubSignInSerializer,
    GoogleSignInSerializer,
    LogoutUserSerializer,
    OTPSerializer,
    PasswordResetRequestSerializer,
    ResendEmailSerializer,
    SetNewPasswordSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)


class UserRegisterSerializerTest(TestCase):
    def setUp(self):
        self.existing_user = CustomUser.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="testpass123",
            first_name="Existing",
            last_name="User",
        )

    def test_valid_registration(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "validpass123",
            "re_password": "validpass123",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("validpass123"))

    def test_username_exists(self):
        data = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "validpass123",
            "re_password": "validpass123",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username"][0]), "This username is already taken"
        )

    def test_email_exists(self):
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "validpass123",
            "re_password": "validpass123",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["email"][0]), "This email is already in use"
        )

    def test_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "validpass123",
            "re_password": "differentpass",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["password"][0], "Passwords do not match.")

    def test_password_too_short(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "123",
            "re_password": "123",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
            is_verified=True,
        )
        self.factory = RequestFactory()

    @patch("django.contrib.auth.authenticate")
    def test_valid_login(self, mock_authenticate):
        mock_authenticate.return_value = self.user
        data = {"email": "test@example.com", "password": "testpass123"}
        request = self.factory.post("/login/")
        serializer = UserLoginSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("access", serializer.data)
        self.assertIn("refresh", serializer.data)

    @patch("django.contrib.auth.authenticate")
    def test_invalid_credentials(self, mock_authenticate):
        mock_authenticate.return_value = None
        data = {"email": "test@example.com", "password": "wrongpass"}
        request = self.factory.post("/login/")
        serializer = UserLoginSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Invalid credentials, please try again",
        )

    @patch("django.contrib.auth.authenticate")
    def test_unverified_user(self, mock_authenticate):
        self.user.is_verified = False
        self.user.save()
        mock_authenticate.return_value = self.user
        data = {"email": "test@example.com", "password": "testpass123"}
        request = self.factory.post("/login/")
        serializer = UserLoginSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Email is not verified"
        )


class OTPSerializerTest(TestCase):
    def test_valid_otp(self):
        data = {"otp": "123456"}
        serializer = OTPSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_otp_too_long(self):
        data = {"otp": "1234567"}
        serializer = OTPSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("otp", serializer.errors)


class PasswordResetSerializerTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        self.url = reverse("password-reset")

    def test_valid_email(self):
        serializer = PasswordResetRequestSerializer(data={"email": "test@example.com"})
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_format(self):
        serializer = PasswordResetRequestSerializer(data={"email": "invalid-email"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_nonexistent_email(self):
        serializer = PasswordResetRequestSerializer(
            data={"email": "nonexistent@example.com"}
        )
        self.assertTrue(serializer.is_valid())  # to avoid attacks


class ResendEmailSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test123",
            email="kacper@gmail.com",
            first_name="Test",
            last_name="User",
            password="2137abcAA!",
        )

    def test_valid_email(self):
        serializer = ResendEmailSerializer(data={"email": "kacper@gmail.com"})
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        serializer = ResendEmailSerializer(data={"email": "this is invalid for sure"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_nonexistent_email(self):
        serializer = ResendEmailSerializer(data={"email": "nonexistent@example.com"})
        self.assertTrue(serializer.is_valid())


class SetNewPasswordSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="oldpassword",
        )
        self.uid = urlsafe_base64_encode(force_bytes(str(self.user.pk)))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.valid_data = {
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "uid": self.uid,
            "token": self.token,
        }

    def test_valid_password_reset(self):
        serializer = SetNewPasswordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.validated_data
        self.assertTrue(user.check_password("newpassword123"))

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data["confirm_password"] = "differentpassword"
        serializer = SetNewPasswordSerializer(data=data)
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Passwords do not match.", str(cm.exception.detail))

    def test_invalid_token(self):
        data = self.valid_data.copy()
        data["token"] = "invalid_token"
        serializer = SetNewPasswordSerializer(data=data)
        with self.assertRaises(AuthenticationFailed) as cm:
            serializer.validate(data)
        self.assertIn("Reset link is invalid or expired", str(cm.exception.detail))

    def test_invalid_uid(self):
        data = self.valid_data.copy()
        data["uid"] = "invalid_uid"
        serializer = SetNewPasswordSerializer(data=data)
        with self.assertRaises(AuthenticationFailed) as cm:
            serializer.validate(data)
        self.assertIn("Reset link is invalid or expired", str(cm.exception.detail))


class LogoutUserSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.valid_data = {"refresh_token": str(self.refresh)}

    def test_valid_logout(self):
        serializer = LogoutUserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.refresh.blacklist()

    def test_invalid_token_logout(self):
        data = {"refresh_token": "invalid_token"}
        serializer = LogoutUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.save()


class GoogleSignInSerializerTests(TestCase):
    @patch("authentication.providers.GoogleAuth.validate")
    def test_valid_google_auth(self, mock_validate):
        mock_validate.return_value = {
            "aud": settings.GOOGLE_CLIENT_ID,
            "email": "google@example.com",
            "given_name": "Google",
            "family_name": "User",
            "sub": "1234567890",
        }

        data = {"access_token": "valid_google_token"}
        serializer = GoogleSignInSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user_data = serializer.validate_access_token("valid_google_token")
        self.assertEqual(user_data["email"], "google@example.com")

    @patch("authentication.providers.GoogleAuth.validate")
    def test_invalid_client_id(self, mock_validate):
        mock_validate.return_value = {"aud": "wrong_client_id"}
        data = {"access_token": "valid_token"}
        serializer = GoogleSignInSerializer(data=data)
        with self.assertRaises(AuthenticationFailed):
            serializer.validate_access_token("valid_token")


class GithubSignInSerializerTests(TestCase):
    @patch("authentication.providers.GithubAuth.retrieve_user_info")
    @patch("authentication.providers.GithubAuth.exchange_code_for_token")
    def test_valid_github_auth(self, mock_exchange, mock_retrieve):
        mock_exchange.return_value = "valid_access_token"
        mock_retrieve.return_value = {
            "login": "githubuser",
            "email": "github@example.com",
            "name": "GitHub User",
        }

        data = {"code": "valid_code"}
        serializer = GithubSignInSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user_data = serializer.validate_code("valid_code")
        self.assertEqual(user_data["email"], "github@example.com")

    @patch("authentication.providers.GithubAuth.exchange_code_for_token")
    def test_invalid_code(self, mock_exchange):
        mock_exchange.return_value = None
        data = {"code": "invalid_code"}
        serializer = GithubSignInSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_code("invalid_code")

    @patch("authentication.providers.GithubAuth.retrieve_user_info")
    @patch("authentication.providers.GithubAuth.exchange_code_for_token")
    def test_missing_email(self, mock_exchange, mock_retrieve):
        mock_exchange.return_value = "valid_token"
        mock_retrieve.return_value = {"login": "githubuser", "name": "User"}
        data = {"code": "valid_code"}
        serializer = GithubSignInSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)
