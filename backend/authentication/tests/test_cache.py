from django.test.testcases import TestCase
from django.core.cache import cache

from ..models import CustomUser
from ..utils import send_code_to_user


class CacheTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            is_verified=False,
        )

    def test_otp_expiration(self):
        send_code_to_user(self.user.email)
        ttl = cache.ttl(f"otp:{self.user.email}")
        self.assertLessEqual(ttl, 600)
