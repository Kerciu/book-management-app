from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Please enter a valid email address")

    def check_field_existence(self, field):
        if not field:
            raise ValueError(
                f'{field.capitalize().replace('_', ' ')} is required.'
            )

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password,
        **other_fields
    ):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("An email is required")

        self.check_field_existence(first_name)
        self.check_field_existence(last_name)
        self.check_field_existence(password)

        user = self.model(
            email,
            first_name,
            last_name,
            password,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
