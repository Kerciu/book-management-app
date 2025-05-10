from django.contrib import admin

from .models import Authors, BookCollections, Books, Categories, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Authors)
admin.site.register(Books)
admin.site.register(BookCollections)
# admin.site.register(BookRatings)
# admin.site.register(BookReviews)
