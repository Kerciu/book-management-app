from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendshipRequest, Friendship, Follow

User = get_user_model()


class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.CharField(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user', 'status', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        to_user = attrs.get('to_user')

        # cannot send a request to yourself
        if to_user == user:
            raise serializers.ValidationError(
                "Cannot send a friend request to yourself.")

        # cannot send if already friends
        if Friendship.are_friends(user, to_user):
            raise serializers.ValidationError("You are already friends with this user.")

        # cannot send duplicate pending request
        if FriendshipRequest.objects.filter(
            from_user=user, to_user=to_user, status='pending'
        ).exists():
            raise serializers.ValidationError(
                "Friend request already sent and pending.")

        return attrs

    def create(self, validated_data):
        # force from_user to be the current user; status defaults to 'pending'
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


class FriendshipSerializer(serializers.ModelSerializer):
    user1 = serializers.StringRelatedField(read_only=True)
    user2 = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    followee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee', 'created_at']
        read_only_fields = ['follower', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        followee = attrs.get('followee')

        # cannot follow yourself
        if followee == user:
            raise serializers.ValidationError("You cannot follow yourself.")

        # cannot double follow
        if Follow.objects.filter(follower=user, followee=followee).exists():
            raise serializers.ValidationError("You are already following this user.")

        return attrs

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)
