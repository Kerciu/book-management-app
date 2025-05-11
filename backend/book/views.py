from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework.pagination import PageNumberPagination

from .models import Book, Author, Publisher, Genre
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
)
from .filters import BookFilter

# Create your views here.


class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return super().has_permission(request, view)

        return request.user.is_staff or request.user.is_superuser


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related(
        "authors",
        "publishers",
        "genres",
    )
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

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

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()


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
