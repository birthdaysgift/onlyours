from django.urls import path

from .views import PageView

app_name = "pages"

urlpatterns = [
    path("<str:username>/", PageView.as_view(), name="page")
]