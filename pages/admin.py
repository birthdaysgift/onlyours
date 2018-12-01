from django.contrib import admin

from .models import Photo, UserPhoto, Video, UserVideo, PostLike, PostDislike,\
    Post, Friendship, FriendshipRequest

admin.site.register(Photo)
admin.site.register(UserPhoto)
admin.site.register(Video)
admin.site.register(UserVideo)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostDislike)
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
