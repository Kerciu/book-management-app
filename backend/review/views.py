from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .serializers import (
    ReviewSerializer,
    ReviewLikeSerializer,
)

from .models import ReviewLike


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def like(self, request, book_pk=None, pk=None):
        review = self.get_object()

        like, created = ReviewLike.objects.get_or_create(
            review=review,
            user=request.user,
        )

        if request.method == "DELETE":
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ReviewLikeSerializer(like, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
