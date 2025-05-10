from unittest.mock import patch

from django.test import TestCase

from ..models import CustomUser, OneTimePassword
from ..utils import generate_otp, send_code_to_user


class EmailUtilsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            first_name="kacper",
            last_name="gorski",
            username="testuser",
            password="testpass123",
        )

    def test_generate_otp_length(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)

    def test_generate_otp_digits(self):
        otp = generate_otp()
        self.assertTrue(otp.isdigit())

    @patch("authentication.utils.EmailMessage")
    def test_send_code_to_user(self, mock_email):
        send_code_to_user(self.user.email)

        self.assertEqual(OneTimePassword.objects.count(), 1)

        mock_email.assert_called_once()
