from rest_framework import viewsets
from .models import Categories, Authors, Books, BookCollections, BookRatings, BookReviews
from .serializers import (
    CategorySerializer, AuthorSerializer, BookSerializer,
    BookCollectionSerializer, BookRatingSerializer, BookReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

class BookCollectionViewSet(viewsets.ModelViewSet):
    queryset = BookCollections.objects.all()
    serializer_class = BookCollectionSerializer

class BookRatingViewSet(viewsets.ModelViewSet):
    queryset = BookRatings.objects.all()
    serializer_class = BookRatingSerializer

class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReviews.objects.all()
    serializer_class = BookReviewSerializer
