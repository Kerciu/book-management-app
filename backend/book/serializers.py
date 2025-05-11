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
    authors = AuthorSerializer(many=True, required=False)
    publishers = PublisherSerializer(many=True, required=False)
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):

        authors_data = validated_data.pop("authors", [])
        publishers_data = validated_data.pop("publishers", [])
        genres_data = validated_data.pop("genres", [])

        book = Book.objects.create(**validated_data)

        for author in authors_data:
            if "id" in author:
                book.authors.add(author["id"])

        for publisher in publishers_data:
            if "id" in publisher:
                book.publishers.add(publisher["id"])

        for genre in genres_data:
            if "id" in genre:
                book.genres.add(genre["id"])

        return book
