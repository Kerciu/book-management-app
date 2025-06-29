from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    GithubSignInView,
    GoogleSignInView,
    GithubLoginCallbackView,
    LoginUserView,
    LogoutUserView,
    PasswordResetConfirmView,
    PasswordResetView,
    ResendEmailView,
    SetNewPasswordView,
    UserRegisterView,
    ValidateRegisterView,
)

urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("verify-user/", ValidateRegisterView.as_view(), name="verify-user"),
    path("resend-email/", ResendEmailView.as_view(), name="resend-email"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uid>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set-new-password"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("google-auth/", GoogleSignInView.as_view(), name="google-auth"),
    path("github-auth/", GithubSignInView.as_view(), name="github-auth"),
    path(
        "github-auth/callback/",
        GithubLoginCallbackView.as_view(),
        name="github-callback",
    ),
]
