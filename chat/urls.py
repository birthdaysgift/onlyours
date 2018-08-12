from django.views.generic.base import RedirectView
from django.urls import path

from .views import ChatView

app_name = "chat"

urlpatterns = [
    path("chat/<int:page>/", ChatView.as_view(), name="chat"),
]
