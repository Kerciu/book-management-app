from django.contrib import admin
from .models import Friendship, FriendshipRequest, Follow

# Register your models here.

admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
admin.site.register(Follow)
