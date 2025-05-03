from google.auth.transport import requests
from google.oauth2 import id_token
from .models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class GoogleAuth():

    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            return "Token is invalid or has expired", str(e)


class OAuth2Registerer():

    @staticmethod
    def register_user(provider, email, username, first_name, last_name):
        user = CustomUser.objects.filter(email=email)

        if user.exists():
            if provider == user[0].auth_provider:
                login_user = authenticate(
                    email=email,
                    password=settings.SOCIAL_AUTH_PASSWORD
                )
                user_tokens = login_user.tokens()

                return {
                    'email': login_user.email,
                    'full_name': login_user.full_name,
                    'refresh': str(user_tokens.get('refresh')),
                    'access': str(user_tokens.get('access'))
                }

            else:
                raise AuthenticationFailed(
                    detail="Please continue your login using " + user[0].auth_provider,
                    code=403
                )

        else:
            new_user = {
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': settings.SOCIAL_AUTH_PASSWORD,
            }

            registered_user = CustomUser.objects.create_user(**new_user)
            registered_user.auth_provider = provider
            registered_user.is_verified = True

            login_user = authenticate(
                email=email,
                password=settings.SOCIAL_AUTH_PASSWORD
            )
            user_tokens = login_user.tokens()

            return {
                'email': login_user.email,
                'full_name': login_user.full_name,
                'refresh': str(user_tokens.get('refresh')),
                'access': str(user_tokens.get('access'))
            }
