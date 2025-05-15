from rest_framework import serializers
from .models import (
    Review,
    ReviewLike,
    ReviewComment,
)


class ReviewSerializer(serializers.Serializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["user", "created_at", "updated_at"]

    def get_likes_count(self, obj):
        return ReviewLike.objects.filter(review=obj).count()

    def get_comments_count(self, obj):
        return ReviewComment.objects.filter(review=obj).count()


class ReviewLikeSerializer(serializers.Serializer):
    pass


class ReviewCommentSerializer(serializers.Serializer):
    pass
