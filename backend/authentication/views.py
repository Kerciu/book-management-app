from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response

# Create your views here.

class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer