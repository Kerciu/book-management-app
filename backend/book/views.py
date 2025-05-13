from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Book, Author, Publisher, Genre
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
)
from .filters import BookFilter

# Create your views here.


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related(
        "authors",
        "publishers",
        "genres",
    )
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    throttle_scope = "books"

    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]

    filterset_class = BookFilter

    search_fields = [
        "title",
        "description",
        "isbn",
        "authors__last_name",
        "genres__name",
    ]

    ordering_fields = [
        "title",
        "published_at",
        "page_count",
        "created_at",
    ]

    ordering = ["title"]

    pagination_class = PageNumberPagination
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.book_set.exists():
            return Response(
                {"error": "Cannot delete genre that is assigned to books."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
