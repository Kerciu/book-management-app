from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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

        present_date = timezone.now().date()
        if birth_date and birth_date > present_date:
            raise serializers.ValidationError("Birth date must not be in the future")
        if death_date and death_date > present_date:
            raise serializers.ValidationError("Death date must not be in the future")

        return attrs


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        extra_kwargs = {
            "name": {
                "validators": [
                    UniqueValidator(
                        queryset=Genre.objects.all(),
                        message="This genre already exists",
                    )
                ]
            }
        }

    def validate_name(self, value):
        existing_name = Genre.objects.filter(name__iexact=value).first()
        if existing_name:
            raise serializers.ValidationError("This genre already exists.")

        return value.lower()


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

    language = serializers.CharField(max_length=30, required=False, default="English")

    page_count = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        error_messages={"min_value": "Page count must be at least 1 if provided."},
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

        if (
            "page_count" in attrs
            and attrs["page_count"] is not None
            and attrs["page_count"] < 1
        ):
            raise serializers.ValidationError("Page count must be at least 1")

        # only validate required relationships on create
        if self.instance is None:  # creation operation
            if not attrs.get("authors"):
                raise serializers.ValidationError("At least one author is required")
            if not attrs.get("genres"):
                raise serializers.ValidationError("At least one genre is required")
        else:  # update operation
            if "authors" in attrs and not attrs["authors"]:
                raise serializers.ValidationError("At least one author is required")
            if "genres" in attrs and not attrs["genres"]:
                raise serializers.ValidationError("At least one genre is required")

        return attrs

    def validate_isbn(self, value):
        import isbnlib

        cleaned_isbn = value.replace("-", "").replace(" ", "")

        if not cleaned_isbn.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits")

        if len(cleaned_isbn) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits long")

        if not isbnlib.is_isbn10(cleaned_isbn) and not isbnlib.is_isbn13(cleaned_isbn):
            raise serializers.ValidationError("Invalid ISBN checksum")

        return cleaned_isbn

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        genres = validated_data.pop("genres", [])
        publishers = validated_data.pop("publishers", [])

        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        book.genres.set(genres)
        book.publishers.set(publishers)
        return book

    def update(self, instance, validated_data):

        authors = validated_data.pop("authors", None)
        genres = validated_data.pop("genres", None)
        publishers = validated_data.pop("publishers", None)

        instance = super().update(instance, validated_data)

        if genres is not None:
            instance.genres.set(genres)

        if authors is not None:
            instance.authors.set(authors)

        if publishers is not None:
            instance.publishers.set(publishers)

        return instance
