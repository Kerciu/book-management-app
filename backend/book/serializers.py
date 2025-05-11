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

    authors_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source="authors",
        many=True,
        write_only=True,
    )

    publishers_ids = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        source="publishers",
        many=True,
        write_only=True,
    )

    genres_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source="genres",
        many=True,
        write_only=True,
    )

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate_isbn(self, value):
        import isbnlib

        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits")

        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits long")

        if not isbnlib.check_digit10(value) and not isbnlib.check_digit13(value):
            raise serializers.ValidationError("Invalid ISBN checksum")

        return value
