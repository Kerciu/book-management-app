from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django.db.models import Q

from .models import FriendshipRequest, Friendship, Follow
from .serializers import (
    FriendshipRequestSerializer,
    FriendshipSerializer,
    FollowSerializer)


class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
    list:
    Return all friendship requests where the current user is
    either the sender or receiver.

    create:
    Send a new friend request to another user.

    retrieve:
    Retrieve a single friendship request (only if you are from_user or to_user).

    accept:
    Accept a pending friendship request (only to_user can do this).

    reject:
    Reject a pending friendship request (only to_user can do this).

    destroy:
    Cancel a pending friendship request (only from_user can do this).
    """
    serializer_class = FriendshipRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendshipRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user)
        )

    def perform_create(self, serializer):
        try:
            serializer.save(from_user=self.request.user)
        except ValidationError as exc:
            raise ValidationError(exc.detail)

    def perform_destroy(self, instance):
        # only allow the sender to cancel a pending request
        user = self.request.user
        if instance.from_user != user:
            raise PermissionDenied("You can only cancel requests you sent.")
        if instance.status != 'pending':
            raise ValidationError("Only pending requests can be cancelled.")
        instance.delete()

    @action(detail=True, methods=['post'], url_path='accept')
    def accept(self, request, pk=None):
        """
        Accept a pending friend request.
        Only the to_user may accept.
        Creates a Friendship and updates status to 'accepted'.
        """
        try:
            fr = FriendshipRequest.objects.get(pk=pk)
        except FriendshipRequest.DoesNotExist:
            raise NotFound("Friend request not found.")

        user = request.user
        if fr.to_user != user:
            raise PermissionDenied("Only the recipient can accept this request.")
        if fr.status != 'pending':
            raise ValidationError("Only pending requests can be accepted.")

        fr.accept()  # This sets status='accepted' and does NOT delete
        return Response({'detail': 'Friend request accepted.'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        Reject a pending friend request.
        Only the to_user may reject.
        Updates status to 'rejected'.
        """
        try:
            fr = FriendshipRequest.objects.get(pk=pk)
        except FriendshipRequest.DoesNotExist:
            raise NotFound("Friend request not found.")

        user = request.user
        if fr.to_user != user:
            raise PermissionDenied("Only the recipient can reject this request.")
        if fr.status != 'pending':
            raise ValidationError("Only pending requests can be rejected.")

        fr.reject()  # This sets status='rejected' and does NOT delete
        return Response({'detail': 'Friend request rejected.'},
                        status=status.HTTP_200_OK)


class FriendshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return all friendships for the current user.

    retrieve:
    Retrieve a specific friendship.
    """
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Friendship.objects.filter(user1=user)
            | Friendship.objects.filter(user2=user)
        )


class FollowViewSet(viewsets.ModelViewSet):
    """
    list:
    List all users the current user follows or is followed by.

    create:
    Follow another user.

    destroy:
    Unfollow a user.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(follower=user)
