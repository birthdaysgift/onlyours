from django.contrib import admin

from .models import Photo, UserPhoto, Video, UserVideo

admin.site.register(Photo)
admin.site.register(UserPhoto)
admin.site.register(Video)
admin.site.register(UserVideo)
