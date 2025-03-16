from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Please enter a valid email address")

    def _check_field_existence(self, field_name, field_value):
        if not field_value:
            readable_name = field_name.replace('_', ' ').capitalize() or "Field"
            raise ValueError(f"{readable_name} is required.")

    def _check_superuser_fields(self, extra_fields, field):
        if extra_fields.get(field) is not True:
            readable_name = field.replace('_', ' ').capitalize()
            raise ValueError(f"{readable_name} must be True for a superuser.")

    def create_user(self, email, first_name, last_name, password=None, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("An email is required.")

        self._check_field_existence("first_name", first_name)
        self._check_field_existence("last_name", last_name)
        self._check_field_existence("password", password)

        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_verified", True)

        self._check_superuser_fields(other_fields, "is_staff")
        self._check_superuser_fields(other_fields, "is_superuser")
        self._check_superuser_fields(other_fields, "is_verified")

        return self.create_user(email, first_name, last_name, password, **other_fields)
