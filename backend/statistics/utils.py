from django.db.models import Count, Q
from shelf.models import Shelf
from book.models import Genre

def recalculate_for(user):

    agg = (
        Shelf.objects
        .filter(user=user, is_default=True)
        .annotate(book_total=Count("books"))
        .values("shelf_type", "book_total")
    )

    counts = {row["shelf_type"]: row["book_total"] for row in agg}

    favourite = (
        Genre.objects
        .filter(book__shelves__user=user,
                book__shelves__is_default=True,
                book__shelves__shelf_type="read")
        .annotate(cnt=Count("book"))
        .order_by("-cnt")
        .first()
    )

    from statistics.models import UserStatistics
    stats, _ = UserStatistics.objects.get_or_create(user=user)
    stats.read = counts.get("read", 0)
    stats.in_progress = counts.get("currently_reading", 0)
    stats.want_to_read = counts.get("want_to_read", 0)
    stats.favourite_genre = favourite
    stats.save(
        update_fields=[
            "read",
            "in_progress",
            "want_to_read",
            "favourite_genre",
        ]
    )