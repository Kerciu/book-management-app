from django.urls import path
from .views import (
    LoginUserView,
    UserRegisterView,
    ValidateRegisterView,
    ResendEmailView,
    PasswordResetView,
    PasswordResetConfirmView,
    SetNewPasswordView
)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('verify-user/', ValidateRegisterView.as_view(), name="verify-user"),
    path('resend-email/', ResendEmailView.as_view(), name='resend-email'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password')
]
