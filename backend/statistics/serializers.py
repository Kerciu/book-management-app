from rest_framework import serializers
from statistics.models import UserStatistics
from book.serializers import GenreSerializer

class UserStatisticsSerializer(serializers.ModelSerializer):
    favourite_genre = GenreSerializer()

    class Meta:
        model = UserStatistics
        fields = (
            "read",
            "in_progress",
            "want_to_read",
            "favourite_genre",
        )
