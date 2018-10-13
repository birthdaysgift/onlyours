from django.contrib import admin

from .models import Photo, UserPhoto

admin.site.register(Photo)
admin.site.register(UserPhoto)
