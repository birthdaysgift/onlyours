from django.contrib import admin

from . import models

admin.site.register(models.Photo)
admin.site.register(models.PhotoLike)
admin.site.register(models.PhotoDislike)
admin.site.register(models.UserPhoto)
