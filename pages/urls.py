from django.urls import path

from .views import EditView, PageView

app_name = "pages"

urlpatterns = [
    path("edit/<int:pk>/", EditView.as_view(), name="edit"),
    path("<str:username>/", PageView.as_view(), name="page"),
]
