from rest_framework.routers import DefaultRouter
from .views import ShelfViewSet

router = DefaultRouter()
router.register(r"shelves", ShelfViewSet, basename="shelf")

urlpatterns = router.urls
