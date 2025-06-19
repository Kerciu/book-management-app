from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FriendshipRequestViewSet, FriendshipViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendshipRequestViewSet, basename='friend-request')
router.register(r'friendships', FriendshipViewSet, basename='friendship')
router.register(r'follows', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
