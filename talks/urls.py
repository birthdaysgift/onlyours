from django.urls import path

from .views import TalksView

app_name = "talks"

urlpatterns = [
    path("talks/", TalksView.as_view(), name="talks_main"),
    path("talks/<str:receiver_name>/<int:page_num>/", TalksView.as_view(),
         name="talks")
]