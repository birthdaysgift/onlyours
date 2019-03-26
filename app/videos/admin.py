from django.contrib import admin

from . import models

admin.site.register(models.Video)
admin.site.register(models.UserVideo)
admin.site.register(models.VideoLike)
admin.site.register(models.VideoDislike)
