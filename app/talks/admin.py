from django.contrib import admin

from .models import PublicMessage, PrivateMessage

admin.site.register(PublicMessage)
admin.site.register(PrivateMessage)
