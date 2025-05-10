from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookCollectionViewSet,
    BookRatingViewSet,
    BookReviewViewSet,
    BookViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"collections", BookCollectionViewSet)
router.register(r"ratings", BookRatingViewSet)
router.register(r"reviews", BookReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
