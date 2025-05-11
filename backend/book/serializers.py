from rest_framework import serializers

from .models import Book, Author, Genre, Publisher


class AuthorSerializer(serializers.Serializer):
    class Meta:
        model = Author
        fields = "__all___"


class GenreSerializer(serializers.Serializer):
    class Meta:
        model = Genre
        fields = "__all___"


class PublisherSerializer(serializers.Serializer):
    class Meta:
        model = Publisher
        fields = "__all___"


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = "__all__"
