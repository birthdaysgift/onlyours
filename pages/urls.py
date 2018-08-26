from django.urls import path

from .views import ChangeView, PageView

app_name = "pages"

urlpatterns = [
    path("<str:username>/", PageView.as_view(), name="page"),
    path("<str:username>/change/", ChangeView.as_view(), name="change")
]
