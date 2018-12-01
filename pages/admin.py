from django.contrib import admin

from .models import Photo, UserPhoto, Video, UserVideo, PostLike, PostDislike

admin.site.register(Photo)
admin.site.register(UserPhoto)
admin.site.register(Video)
admin.site.register(UserVideo)
admin.site.register(PostLike)
admin.site.register(PostDislike)
