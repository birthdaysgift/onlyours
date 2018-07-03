from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Index page name"),
    path("login/", views.login, name="Login page name"),
    path("register/", views.register, name="Register page name")
]
