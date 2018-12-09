from django.contrib import admin

from .models import Video, UserVideo, Friendship, FriendshipRequest

admin.site.register(Video)
admin.site.register(UserVideo)
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
