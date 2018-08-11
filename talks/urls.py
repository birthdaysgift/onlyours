from django.urls import path

from .views import TalksView

app_name = "talks"

urlpatterns = [
    path("talks/", TalksView.as_view()),
    path("talks/<str:receiver_name>/", TalksView.as_view(), name="talks")
]