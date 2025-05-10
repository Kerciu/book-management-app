from django.conf import settings
from django.contrib.auth import authenticate

# from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import CustomUser
from .providers import GithubAuth, GoogleAuth, OAuth2Registerer


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    re_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "re_password",
        ]
        extra_kwargs = {
            "username": {"validators": []},
            "email": {"validators": []},
            "re_password": {"write_only": True},
        }

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value

    # def validate_password(self, value):
    #     validate_password(value)
    #     return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("re_password"):
            raise serializers.ValidationError({"password": ["Passwords do not match."]})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "full_name", "access", "refresh"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        request = self.context.get("request")
        user = authenticate(request, email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials, please try again")

        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified")

        user_tokens = user.tokens()

        return {
            "email": user.email,
            "full_name": user.full_name,
            "refresh": str(user_tokens.get("refresh")),
            "access": str(user_tokens.get("access")),
        }


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "confirm_password", "uid", "token"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"non_field_errors": ["Passwords do not match."]}
            )

        try:
            user_id = force_str(urlsafe_base64_decode(attrs["uid"]))
            user_id = int(user_id)
            user = CustomUser.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
                raise AuthenticationFailed("Reset link is invalid or expired", 401)

            user.set_password(attrs["password"])
            user.save()
            return user
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise AuthenticationFailed("Reset link is invalid or expired", 401)


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"bad_token": "Token is invalid or expired"}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail("bad_token")


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        google_user_data = GoogleAuth.validate(access_token)

        if not isinstance(google_user_data, dict):
            raise serializers.ValidationError("This token is invalid or has expired")

        if google_user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail="Could not authenticate user", code=401)

        email = google_user_data["email"]
        first_name = google_user_data["given_name"]
        last_name = google_user_data["family_name"]
        provider = "google"
        username = google_user_data["sub"]

        return OAuth2Registerer.register_user(
            provider=provider,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )


class GithubSignInSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=2)

    def validate_code(self, code):
        access_token = GithubAuth.exchange_code_for_token(code)
        if access_token is None:
            raise serializers.ValidationError("This token is invalid or has expired")

        user_info = GithubAuth.retrieve_user_info(access_token)

        email = user_info.get("email")
        if not email:
            raise serializers.ValidationError("Email is required for registration")

        username = user_info.get("login")
        provider = "github"

        full_name = user_info.get("name", "")
        if full_name:
            name_parts = full_name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
        else:
            first_name = last_name = ""

        return OAuth2Registerer.register_user(
            provider=provider,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
