from django.test import TestCase
from ...models import CustomUser
from ...serializers import ResendEmailSerializer
from django.core.exceptions import ValidationError
