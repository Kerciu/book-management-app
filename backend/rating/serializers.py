class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRatings
        fields = '__all__'