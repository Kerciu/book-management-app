from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginUserView, UserRegisterView, ValidateRegisterView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('verify-user/', ValidateRegisterView.as_view(), name="verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
