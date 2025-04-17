from rest_framework.generics import GenericAPIView
from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword

# Create your views here.

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
    serializer_class=UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

