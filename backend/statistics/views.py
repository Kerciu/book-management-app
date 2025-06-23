from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from statistics.serializers import UserStatisticsSerializer
from statistics.models import UserStatistics

class MyStatsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserStatisticsSerializer

    def get_object(self):
        stats, _ = UserStatistics.objects.get_or_create(user=self.request.user)
        return stats


class UserStatsView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserStatisticsSerializer
    queryset = UserStatistics.objects.select_related("user")

    lookup_field = "user_id"  