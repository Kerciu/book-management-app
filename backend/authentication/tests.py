from django.test import TestCase
from .models import CustomUser
from .serializers import ResendEmailSerializer

# Create your tests here.

class ResendEmailSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test123",
            email="kacper@gmail.com",
            first_name='Test',
            last_name='User',
            password="2137abcAA!"
        )

    def test_is_valid_email(self):
        pass
    