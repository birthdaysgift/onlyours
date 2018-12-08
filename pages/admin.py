from django.contrib import admin

from .models import Photo, UserPhoto, Video, UserVideo,\
    Friendship, FriendshipRequest

admin.site.register(Photo)
admin.site.register(UserPhoto)
admin.site.register(Video)
admin.site.register(UserVideo)
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
