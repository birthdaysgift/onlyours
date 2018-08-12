from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import IndexView, LoginView, RegisterView

app_name = "auth_custom"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/",
         LogoutView.as_view(next_page=reverse_lazy("auth_custom:login")),
         name="logout"),
    path("register/", RegisterView.as_view(), name="register")
]