import logging

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.core.cache import cache

from .models import CustomUser
from .serializers import (
    GithubSignInSerializer,
    GoogleSignInSerializer,
    LogoutUserSerializer,
    OTPSerializer,
    PasswordResetRequestSerializer,
    ResendEmailSerializer,
    SetNewPasswordSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from .utils import (
    generate_password_reset_tokens,
    send_code_to_user,
    send_password_reset_email,
)

logger = logging.getLogger(__name__)


class UserRegisterView(GenericAPIView):

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_code_to_user(user.email)
            return Response(
                {
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "message": "Check your email for your verification passcode",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateRegisterView(GenericAPIView):

    serializer_class = OTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp")

        stored_otp = cache.get(f"otp:{email}")
        if stored_otp and stored_otp == otp_code:
            user = CustomUser.objects.get(email=email)

            if user.is_verified:
                cache.delete(f"otp:{email}")
                return Response(
                    {"message": "Account is already verified"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )

            user.is_verified = True
            user.save()
            cache.delete(f"otp:{email}")
            return Response(
                {"message": "Account verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Passcode not provided or has expired"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LoginUserView(GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data
            return Response(
                {"message": "Logged in successfully", "user": user_data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailView(GenericAPIView):
    serializer_class = ResendEmailSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]  # anti-spam

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            send_code_to_user(email, resending=True)
            return Response(
                {"message": "New verification code has been sent to your email"},
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"OTP resend failed: {str(e)}")
            return Response(
                {"message": "Failed to resend OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetView(GenericAPIView):

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.get(email=email)
            uid, token = generate_password_reset_tokens(user)
            try:
                send_password_reset_email(user, uid, token, request)
            except Exception as e:
                logger.error(f"Failed to send password reset email: {str(e)}")

        except CustomUser.DoesNotExist:
            pass  # still returns 200

        return Response(
            {"message": "If this email exists, a reset link has been sent"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):

    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return self._invalid_token_response()

            return Response(
                {
                    "success": True,
                    "message": "Credentials are valid",
                    "uid": uid,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )

        except (DjangoUnicodeDecodeError, CustomUser.DoesNotExist, ValueError):
            return self._invalid_token_response()

    def _invalid_token_response(self):
        return Response(
            {"success": False, "message": "Token is invalid or has expired"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class SetNewPasswordView(GenericAPIView):

    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "Password reset sucessfully"}, status=status.HTTP_200_OK
        )


class LogoutUserView(GenericAPIView):

    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_205_RESET_CONTENT)


class GoogleSignInView(GenericAPIView):
    serializer_class = GoogleSignInSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GithubSignInView(GenericAPIView):
    serializer_class = GithubSignInSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GithubLoginCallbackView(GenericAPIView):
    serializer_class = GithubSignInSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Code parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data={"code": code})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
