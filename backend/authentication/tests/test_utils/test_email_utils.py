from django.test import TestCase
from ...utils import generate_otp

class EmailUtilsTest(TestCase):
    def test_generate_otp_length(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)
