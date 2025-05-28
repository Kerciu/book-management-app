from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"reviews/(?P<book_pk>\d+)/reviews", ReviewViewSet, basename="reviews")
router.register(
    r"reviews/(?P<review_pk>\d+)/comments", CommentViewSet, basename="comments"
)

urlpatterns = [path("", include(router.urls))]
