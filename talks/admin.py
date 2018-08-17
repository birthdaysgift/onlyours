from django.contrib import admin

from auth_custom.models import User

from .models import PublicMessage, PrivateMessage


admin.site.register(User)
admin.site.register(PublicMessage)
admin.site.register(PrivateMessage)
