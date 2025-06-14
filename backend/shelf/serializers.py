from rest_framework import serializers
from .models import Shelf
from book.models import Book


class ShelfSerializer(serializers.ModelSerializer):
    shelf_type = serializers.ChoiceField(
        choices=Shelf.SHELF_TYPES,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Shelf
        fields = [
            'id', 'user', 'name', 'is_default',
            'shelf_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        instance = self.instance

        is_default = attrs.get('is_default', False)
        shelf_type = attrs.get('shelf_type')
        name = attrs.get('name')

        if is_default:
            if not shelf_type:
                raise serializers.ValidationError(
                    "Default shelves must have a shelf type"
                )

            attrs['name'] = dict(Shelf.SHELF_TYPES).get(shelf_type, name)

            if Shelf.objects.filter(
                user=user,
                shelf_type=shelf_type,
                is_default=True
            ).exclude(pk=instance.pk if instance else None).exists():
                raise serializers.ValidationError(
                    "Default shelf of this type already exists"
                )
        else:
            if shelf_type:
                raise serializers.ValidationError(
                    "Custom shelves cannot have a shelf type"
                )
            if name and Shelf.objects.filter(
                user=user,
                name__iexact=name
            ).exclude(pk=instance.pk if instance else None).exists():
                raise serializers.ValidationError(
                    "You already have a shelf with this name"
                )

        return attrs

    def validate_is_default(self, value):
        if self.instance and self.instance.is_default and not value:
            raise serializers.ValidationError(
                "Cannot convert default shelf to custom"
            )
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_default:
            if 'shelf_type' in validated_data:
                raise serializers.ValidationError(
                    "Cannot modify shelf type for default shelves"
                )
            if 'name' in validated_data:
                raise serializers.ValidationError(
                    "Cannot rename default shelves"
                )
        return super().update(instance, validated_data)


class AddBookToShelfSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def validate(self, attrs):
        shelf = self.context['shelf']
        book = attrs['book_id']
        if shelf.books.filter(pk=book.pk).exists():
            raise serializers.ValidationError("This book is already on the shelf.")
        return attrs


class RemoveBookFromShelfSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
