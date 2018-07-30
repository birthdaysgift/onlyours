from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<int:page>/", views.ChatView.as_view(), name="chat"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register")
]
