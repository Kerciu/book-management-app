from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from django.shortcuts import get_object_or_404

from .permissions import IsCommentOwner, IsReviewOwner
from .throttles import CommentCreateThrottle
from .pagination import CommentPagination
from .serializers import ReviewSerializer, ReviewLikeSerializer, ReviewCommentSerializer

from book.models import Book
from .models import Review, ReviewLike, ReviewComment


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            Review.objects.filter(book_id=self.kwargs["book_pk"])
            .select_related("user")
            .prefetch_related("likes", "comments")
        )

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        serializer.save(user=self.request.user, book=book)

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def like(self, request, book_pk=None, pk=None):
        review = self.get_object()

        if request.method == "POST":
            like, created = ReviewLike.objects.get_or_create(
                review=review, user=request.user
            )
            if not created:
                return Response(
                    {"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                ReviewLikeSerializer(like).data, status=status.HTTP_201_CREATED
            )

        if request.method == "DELETE":
            deleted, _ = ReviewLike.objects.filter(
                review=review, user=request.user
            ).delete()
            if deleted == 0:
                return Response(
                    {"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsReviewOwner()]
        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    serializer_class = ReviewCommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        qs = ReviewComment.objects.filter(review_id=self.kwargs["review_pk"]).order_by(
            "-created_at"
        )

        if search := self.request.query_params.get("search"):
            qs = qs.filter(text__icontains=search)

        return qs

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs["review_pk"])
        serializer.save(user=self.request.user, review=review)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["review"] = get_object_or_404(Review, pk=self.kwargs["review_pk"])
        return context

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsCommentOwner()]
        return super().get_permissions()

    def get_throttles(self):
        if self.action == "create":
            return [CommentCreateThrottle()]
        return super().get_throttles()
