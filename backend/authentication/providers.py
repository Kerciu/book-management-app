import requests as api_requests
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


class GoogleAuth:

    @staticmethod
    def validate(token):
        try:
            id_info = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=300,
            )

            client_id = settings.GOOGLE_CLIENT_ID
            aud = id_info["aud"]

            if isinstance(aud, list):
                if client_id not in aud:
                    return None
            elif aud != client_id:
                return None

            return id_info

        except Exception:
            return None


class GithubAuth:

    @staticmethod
    def exchange_code_for_token(code):
        param_payload = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        }

        try:

            res = api_requests.post(
                settings.GITHUB_TOKEN_URL,
                data=param_payload,
                headers={"Accept": "application/json"},
            )

            if res.status_code != 200:
                raise AuthenticationFailed(f"GitHub token exchange failed: {res.text}")

            payload = res.json()
            token = payload.get("access_token")
            if not token:
                raise AuthenticationFailed(f"GitHub token missing: {payload}")

            return token

        except Exception as e:
            raise AuthenticationFailed(f"GitHub authentication failed: {str(e)}")

    @staticmethod
    def retrieve_user_info(access_token):
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            user_res = api_requests.get("https://api.github.com/user", headers=headers)
            if user_res.status_code != 200:
                raise AuthenticationFailed(
                    f"""
                    Failed to fetch user data: {user_res.status_code} - {user_res.text}
                """
                )

            user_data = user_res.json()
            username = user_data.get("login", "githubuser")

            email_res = api_requests.get(
                "https://api.github.com/user/emails", headers=headers
            )
            email_data = email_res.json() if email_res.status_code == 200 else []

            primary_email = None
            for email_info in email_data:
                if email_info.get("primary") and email_info.get("verified"):
                    primary_email = email_info["email"]
                    break

            if primary_email:
                user_data["email"] = primary_email
            else:
                user_data["email"] = f"{username}@users.noreply.github.com"

            return user_data

        except Exception as e:
            raise AuthenticationFailed(f"GitHub API error: {str(e)}")


class OAuth2Registerer:
    @staticmethod
    def login_user(email):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("User not found")

        tokens = user.tokens()
        return {
            "email": user.email,
            "full_name": user.full_name,
            "refresh": tokens["refresh"],
            "access": tokens["access"],
        }

    @staticmethod
    def register_user(provider, email, username, first_name, last_name):
        try:
            user = CustomUser.objects.get(email=email)
            if user.auth_provider != provider:
                raise AuthenticationFailed(
                    detail=f"Please continue with {user.auth_provider}",
                    code=403,
                )
            return OAuth2Registerer.login_user(email)
        except CustomUser.DoesNotExist:
            new_user = CustomUser.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                auth_provider=provider,
                password=None,
            )
            new_user.is_verified = True
            new_user.save()
            return OAuth2Registerer.login_user(email)
