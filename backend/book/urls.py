from rest_framework.routers import DefaultRouter

from .views import BookViewSet, AuthorViewSet, PublisherViewSet, GenreViewSet

router = DefaultRouter()

router.register(r"books", BookViewSet, basename="books")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"publishers", PublisherViewSet, basename="publishers")
router.register(r"genres", GenreViewSet, basename="genres")

urlpatterns = router.urls
