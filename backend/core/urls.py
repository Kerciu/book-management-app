from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/book/", include("book.urls")),
    path("api/shelf/", include("shelf.urls")),
    path("api/social/", include("social.urls")),
    path("api/review/", include("review.urls")),
    # Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(), name="schema-redoc"),
    path("api/schema/swagger-ui", SpectacularSwaggerView.as_view(), name="schema-json"),
]
