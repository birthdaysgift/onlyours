from django.urls import path

from .views import EditView, PageView

app_name = "pages"

urlpatterns = [
    path("<str:username>/", PageView.as_view(), name="page"),
    path("<str:username>/edit/", EditView.as_view(), name="edit")
]
