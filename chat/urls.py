from django.views.generic.base import RedirectView
from django.urls import path

from .views import ChatView

app_name = "chat"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="auth_custom:login")),
    path("chat/<int:page>/", ChatView.as_view(), name="chat"),
]
