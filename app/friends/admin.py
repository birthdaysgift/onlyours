from django.contrib import admin

from .models import Friendship, FriendshipRequest

admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
