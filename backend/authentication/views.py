from rest_framework.generics import GenericAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import AllowAny
from .serializers import (
    UserLoginSerializer,
    UserRegisterSerializer,
    OTPSerializer,
    ResendEmailSerializer,
    PasswordResetRequestSerializer
)

from rest_framework.response import Response
from rest_framework import status
from .utils import (
    send_code_to_user,
    generate_password_reset_tokens,
    send_password_reset_email
)
from .models import OneTimePassword, CustomUser
import logging

# TODO: implement all this in utils file
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import (
    smart_str,
    DjangoUnicodeDecodeError
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# TODO

logger = logging.getLogger(__name__)

class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):

        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])

            return Response({
                'data': user_data,
                'message': "Check your email for your verification passcode"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateRegisterView(GenericAPIView):
    serializer_class = OTPSerializer

    def post(self, request):
        otp_code = request.data.get('otp')

        try:
            otp_code_object = OneTimePassword.objects.get(code=otp_code)
            user = otp_code_object.user

            if user.is_verified:
                return Response({'message': 'Account is already verified'}, status=status.HTTP_204_NO_CONTENT)

            user.is_verified = True
            user.save()

            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)

        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Passcode not provided'}, status=status.HTTP_404_NOT_FOUND)


class LoginUserView(GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data
            return Response({
                'message': 'Logged in successfully',
                'user': user_data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailView(GenericAPIView):

    serializer_class = ResendEmailSerializer

    def post(self, request):
        
        serialzier = self.serializer_class(data=request.data)
        if serialzier.is_valid(raise_exception=True):
            
            email = serialzier.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                
                OneTimePassword.objects.filter(user=user).delete()

                send_code_to_user(email, resending=True)

                return Response({
                    "message": "New verification code has been sent to your email"
                }, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({
                    "message": "User with this email does not exist!"
                }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(GenericAPIView):

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            uid, token = generate_password_reset_tokens(user)
            send_password_reset_email(user, uid, token, request)

            return Response(
                {"message": "If this email exists, a reset link has been sent"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return Response(
                {"message": "If this email exists, a reset link has been sent"},
                status=status.HTTP_200_OK
            )


class PasswordResetConfirmView(GenericAPIView):

    def get(self, request, uid, token):
        pass
