from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Book, Author, Publisher, Genre
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
)

# Create your views here.


class BookViewSet(viewsets.ViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = IsAuthenticated


class AuthorViewSet(viewsets.ViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = IsAuthenticated


class PublisherViewSet(viewsets.ViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = IsAuthenticated


class GenreViewSet(viewsets.ViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = IsAuthenticated
