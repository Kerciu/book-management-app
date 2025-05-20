from rest_framework import serializers
from .models import (
    Review,
    ReviewLike,
    ReviewComment,
)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "text",
            "has_spoilers",
            "is_public",
            "likes_count",
            "comments_count",
            "has_liked",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["user", "created_at", "updated_at"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_has_liked(self, obj):
        request = self.context.get("request")
        return (
            request
            and request.user.is_authenticated
            and obj.likes.filter(user=request.user).exists()
        )


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReviewLike
        fields = [
            "id",
            "user",
            "review",
            "created_at",
        ]
        read_only_fields = ["user", "review", "created_at"]


class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = [
            "id",
            "user",
            "review",
            "text",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "review", "created_at", "updated_at"]

    def get_can_edit(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.user

    def validate(self, attrs):

        review = self.context.get("review")
        user = self.context.get("request").user

        if not review.is_public and user != review.user:
            raise serializers.ValidationError(
                "Cannot comment on private reviews unless you're the owner"
            )

        return attrs
