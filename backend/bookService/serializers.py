from rest_framework import serializers
from .models import Categories, Authors, Books, BookCollections, BookRatings, BookReviews, Users

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCollections
        fields = '__all__'

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRatings
        fields = '__all__'

class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReviews
        fields = '__all__'
