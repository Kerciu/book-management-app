from django.urls import path
from .views import (
    LoginUserView,
    UserRegisterView,
    ValidateRegisterView,
    ResendEmailView
)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('verify-user/', ValidateRegisterView.as_view(), name="verify"),
    path('resend-email/', ResendEmailView.as_view(), name='resend'),
]
