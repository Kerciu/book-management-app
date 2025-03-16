from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
