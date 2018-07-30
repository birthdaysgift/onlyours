from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index-page-url"),
    path("chat/<int:page>/", views.ChatView.as_view(), name="chat-page-url"),
    path("login/", views.LoginView.as_view(), name="login-page-url"),
    path("logout/", views.logout, name="logout-page-url"),
    path("register/", views.RegisterView.as_view(), name="register-page-url")
]
