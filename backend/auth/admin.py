from django.contrib import admin

from .models import CustomUser, OneTimePassword

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(OneTimePassword)
