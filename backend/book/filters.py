from django_filters import rest_framework as filters
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import Book, Genre
from .serializers import GenreSerializer


class BookFilter(filters.FilterSet):
    min_pages = filters.NumberFilter(
        field_name="page_count", lookup_expr="gte")
    max_pages = filters.NumberFilter(
        field_name="page_count", lookup_expr="lte")

    published_after = filters.DateFilter(
        field_name="published_at",
        lookup_expr="gte",
        label="Publish on or after (YYYY-MM-DD)",
        method="validate_published_after",
    )

    published_before = filters.DateFilter(
        field_name="published_at",
        lookup_expr="lte",
        label="Publish on or before (YYYY-MM-DD)",
        method="validate_published_before",
    )

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "isbn": ["exact"],
            "language": ["exact"],
            "authors__last_name": ["icontains"],
            "genres__name": ["exact"],
            "page_count": ["exact"],
        }

    def validate_published_after(self, queryset, name, value):
        return queryset.filter(**{"published_at__gte": value})

    def validate_published_before(self, queryset, name, value):
        if value > timezone.now().date():
            raise ValidationError(
                "Published before date cannot be in the future")
        return queryset.filter(**{"published_at__lte": value})


class GenreFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Genre
        fields = ['name']
