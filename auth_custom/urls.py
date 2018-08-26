from django.contrib.auth.views import LogoutView
from django.urls import path, reverse, reverse_lazy

from .views import LoginView, RegisterView

app_name = "auth_custom"

urlpatterns = [

    path("login/", LoginView.as_view(), name="login"),
    path("logout/",
         LogoutView.as_view(next_page=reverse_lazy("auth_custom:login")),
         name="logout"),
    path("register/", RegisterView.as_view(), name="register")
]