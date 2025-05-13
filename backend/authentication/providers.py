import requests as api_requests
from django.conf import settings
from django.contrib.auth import authenticate
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


class GoogleAuth:

    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            if "accounts.google.com" in id_info["iss"]:
                return id_info

        except Exception as e:
            return "Token is invalid or has expired", str(e)


class GithubAuth:

    @staticmethod
    def exchange_code_for_token(code):
        param_payload = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        }

        res = requests.post(
            settings.GITHUB_TOKEN_URL,
            data=param_payload,
            headers={"Accept": "application/json"},
        )

        payload = res.json()
        return payload.get("access_token")

    @staticmethod
    def retrieve_user_info(access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        try:
            res = api_requests.get(settings.GITHUB_USER_URL, headers=headers)

            return res.json()

        except Exception as e:
            return AuthenticationFailed("Token is invalid or has expired", str(e))


class OAuth2Registerer:

    @staticmethod
    def login_user(email, password):
        user = authenticate(email=email, password=password)
        tokens = user.tokens()

        return {
            "email": user.email,
            "full_name": user.full_name,
            "refresh": str(tokens.get("refresh")),
            "access": str(tokens.get("access")),
        }

    @staticmethod
    def register_user(provider, email, username, first_name, last_name):
        user = CustomUser.objects.filter(email=email)

        if user.exists():
            if provider == user[0].auth_provider:
                return OAuth2Registerer.login_user(email, settings.SOCIAL_AUTH_PASSWORD)

            else:
                raise AuthenticationFailed(
                    detail="Please continue your login using " + user[0].auth_provider,
                    code=403,
                )

        else:
            new_user = {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password": settings.SOCIAL_AUTH_PASSWORD,
                "provider": provider,
            }

            registered_user = CustomUser.objects.create_user(**new_user)
            registered_user.auth_provider = provider
            registered_user.is_verified = True

            registered_user.save()

            return OAuth2Registerer.login_user(
                email=registered_user.email, password=settings.SOCIAL_AUTH_PASSWORD
            )
