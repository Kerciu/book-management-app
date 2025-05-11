from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    published_after = filters.DateFilter(
        field_name="published_at",
        lookup_expr="gte",
    )

    published_before = filters.DateFilter(field_name="published_at", lookup_expr="lte")

    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "isbn": ["exact"],
            "language": ["exact"],
            "authors__last_name": ["icontains"],
            "genres__name": ["exact"],
        }
