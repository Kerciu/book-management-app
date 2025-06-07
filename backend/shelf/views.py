from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Shelf
from .serializers import ShelfSerializer,  AddBookToShelfSerializer
from book.serializers import BookSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            raise ValidationError(e.detail)

    def perform_destroy(self, instance):
        if instance.is_default:
            raise ValidationError("Cannot delete default shelves")
        instance.delete()

    @action(detail=True, methods=["get"])
    def books(self, request, pk=None):
        """GET /shelves/{id}/books/ - List books on a shelf"""
        shelf = self.get_object()
        books = shelf.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_book(self, request, pk=None):
        """POST /shelves/{id}/add_book/ - Add a book to the shelf"""
        shelf = self.get_object()
        serializer = AddBookToShelfSerializer(
            data=request.data, context={'shelf': shelf})
        serializer.is_valid(raise_exception=True)
        shelf.books.add(serializer.validated_data['book_id'])
        return Response({"detail": "Book added to shelf."}, status=status.HTTP_200_OK)
