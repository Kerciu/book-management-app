from django.urls import path
from .views import MyStatsView, UserStatsView

urlpatterns = [
    path("stats/", MyStatsView.as_view(), name="my-stats"),

    path(
        "users/<int:user_id>/stats/",
        UserStatsView.as_view(),
        name="user-stats",
    ),
]