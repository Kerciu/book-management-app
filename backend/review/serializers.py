class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReviews
        fields = '__all__'
