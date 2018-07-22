from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Index page name"),
    path("chat/", views.ChatView.as_view(), name="Chat page name"),
    path("login/", views.LoginView.as_view(), name="Login page name"),
    path("logout/", views.logout, name="Logout page name"),
    path("register/", views.RegisterView.as_view(), name="Register page name")
]
