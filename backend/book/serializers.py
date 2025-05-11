from rest_framework import serializers

from .models import Book, Author, Genre, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)
    publishers = PublisherSerializer(many=True, required=False)
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):

        authors = validated_data.pop("authors", [])
        publishers = validated_data.pop("publishers", [])
        genres = validated_data.pop("genres", [])

        book = Book.objects.create(**validated_data)

        book.authors.add(authors)
        book.publishers.add(publishers)
        book.genres.add(genres)

        return book

    def validate_isbn(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits")

        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits long")

        return value
