from django.urls import path

from .dbhelpers import add_private_messages, add_public_messages
from .views import TalksView

app_name = "talks"

urlpatterns = [
    path("<str:receiver_name>/<int:page_num>/", TalksView.as_view(),
         name="talk")
]

helpers = [
    path("add_private_messages/<str:u1>/<str:u2>/", add_private_messages),
    path(
        "add_public_messages/<str:u1>/<str:u2>/<str:u3>/", add_public_messages
    ),
]

urlpatterns += helpers
