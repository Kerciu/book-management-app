from django.test import TestCase
from .models import CustomUser
from .serializers import ResendEmailSerializer

# Create your tests here.

class ResendEmailSerializerTest(TestCase):

    user = CustomUser.objects.create_user(
        username="test123",
        email="kacper@gmail.com",
        first_name='Test',
        last_name='User',
        password="2137abcAA!"
    )

    