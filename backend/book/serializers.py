from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator

from .models import Book, Author, Genre, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def validate(self, attrs):
        birth_date = attrs.get("birth_date")
        death_date = attrs.get("death_date")

        if birth_date and death_date and death_date < birth_date:
            raise serializers.ValidationError("Death date must be after birth date")

        return attrs


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"

    def validate_website(self, value):
        validator = URLValidator()
        validator(value)
        return value


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)
    publishers = PublisherSerializer(many=True, required=False)
    genres = GenreSerializer(many=True, required=False)

    authors_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source="authors",
        many=True,
        write_only=True,
        required=True,
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
        required=True,
    )

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        published_at = attrs.get("published_at")
        if published_at and published_at > timezone.now().date():
            raise serializers.ValidationError(
                "Publication date cannot be in the future"
            )

        if not attrs.get("authors"):
            raise serializers.ValidationError("At least one author is required")

        return attrs

    def validate_isbn(self, value):
        import isbnlib

        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits")

        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits long")

        if not isbnlib.is_isbn10(value) and not isbnlib.is_isbn13(value):
            raise serializers.ValidationError("Invalid ISBN checksum")

        return value
