from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FriendshipRequestViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendshipRequestViewSet, basename='friend-request')

urlpatterns = [
    path('', include(router.urls)),
]
