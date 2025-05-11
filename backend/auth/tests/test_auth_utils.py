from unittest.mock import patch, ANY

from django.test import TestCase, RequestFactory

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings

from ..models import CustomUser, OneTimePassword
from ..utils import (
    generate_otp,
    send_code_to_user,
    generate_password_reset_tokens,
    send_password_reset_email,
)


class EmailUtilsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            username="testuser",
            password="testpass123",
        )
        self.factory = RequestFactory()

        self.site = Site.objects.get(id=1)
        self.site.domain = "testserver"
        self.site.name = "testserver"
        self.site.save()

    def test_generate_otp_length(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)

    def test_generate_otp_digits(self):
        otp = generate_otp()
        self.assertTrue(otp.isdigit())
        self.assertTrue(all(c in "0123456789" for c in otp))

    @patch("authentication.utils.EmailMessage")
    def test_send_code_to_user(self, mock_email):
        send_code_to_user(self.user.email)

        otp = OneTimePassword.objects.first()
        self.assertIsNotNone(otp)
        self.assertEqual(otp.user, self.user)
        self.assertEqual(len(otp.code), 6)

        mock_email.assert_called_once_with(
            subject="One time passcode for email verification",
            body=ANY,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email],
        )

    @patch("authentication.utils.EmailMessage")
    def test_send_code_resending(self, mock_email):
        send_code_to_user(self.user.email, resending=True)

        body = mock_email.call_args[1]["body"]
        self.assertIn("Thank you Test", body)

    def test_generate_password_reset_tokens(self):
        uid, token = generate_password_reset_tokens(self.user)

        self.assertEqual(uid, urlsafe_base64_encode(force_bytes(self.user.pk)))

        self.assertTrue(PasswordResetTokenGenerator().check_token(self.user, token))

    @patch("authentication.utils.EmailMessage")
    def test_send_password_reset_email(self, mock_email):
        request = self.factory.get("/")
        uid, token = generate_password_reset_tokens(self.user)
        send_password_reset_email(self.user, uid, token, request)

        called_args = mock_email.call_args[1]
        subject = called_args["subject"]
        body = called_args["body"]
        from_email = called_args["from_email"]
        to = called_args["to"]

        self.assertEqual(subject, "Password Reset Request")
        self.assertEqual(from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(to, [self.user.email])

        self.assertIn("Hello Test!", body)
        self.assertIn("Use this link to reset your password", body)

        expected_path = reverse(
            "password-reset-confirm", kwargs={"uid": uid, "token": token}
        )
        self.assertIn(expected_path, body)
        self.assertIn(f"http://testserver{expected_path}", body)

    def test_generate_password_reset_tokens_unique(self):
        uid1, token1 = generate_password_reset_tokens(self.user)

        self.user.set_password("new_password")
        self.user.save()

        uid2, token2 = generate_password_reset_tokens(self.user)

        self.assertEqual(uid1, uid2)
        self.assertNotEqual(token1, token2)
