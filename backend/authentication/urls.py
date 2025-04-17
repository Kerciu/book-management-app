from django.urls import path
from .views import UserRegisterView, ValidateRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('verify-user/', ValidateRegisterView.as_view(), name="verify")
]