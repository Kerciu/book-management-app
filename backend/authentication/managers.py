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
        if not field_value and field_name != "password":
            readable_name = field_name.replace("_", " ").capitalize() or "Field"
            raise ValueError(f"{readable_name} is required.")

    def _check_superuser_fields(self, extra_fields, field):
        if extra_fields.get(field) is not True:
            readable_name = field.replace("_", " ").capitalize()
            raise ValueError(f"{readable_name} must be True for a superuser.")

    def create_user(
        self, username, email, first_name, last_name, password=None, **other_fields
    ):

        auth_provider = other_fields.get("auth_provider", "email")

        if not username:
            raise ValueError("Username is required.")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("An email is required.")

        self._check_field_existence("first_name", first_name)
        self._check_field_existence("last_name", last_name)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **other_fields,
        )

        if auth_provider == "email" and password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, first_name, last_name, password=None, **other_fields
    ):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_verified", True)

        self._check_superuser_fields(other_fields, "is_staff")
        self._check_superuser_fields(other_fields, "is_superuser")
        self._check_superuser_fields(other_fields, "is_verified")

        return self.create_user(
            username, email, first_name, last_name, password, **other_fields
        )
