from django.test import TestCase
from .models import CustomUser
from .serializers import ResendEmailSerializer
from django.core.exceptions import ValidationError

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

    def test_valid_email(self):
        serializer = ResendEmailSerializer.create(data={ "email": "kerciu@gmail.com"})
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_email(self):
        serializer = ResendEmailSerializer.create(data={ "email": "this is invalid for sure"})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_nonexistent_email(self):
        serializer = ResendEmailSerializer(data={'email': 'nonexistent@example.com'})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
