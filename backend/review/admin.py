from django.contrib import admin
from .models import Review, ReviewLike, ReviewComment


# Register your models here.

admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(ReviewComment)
