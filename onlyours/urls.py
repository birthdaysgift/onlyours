from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("auth_custom.urls")),
    path("", include("pages.urls")),
    path("", include("talks.urls")),
    path('admin/', admin.site.urls)
]
