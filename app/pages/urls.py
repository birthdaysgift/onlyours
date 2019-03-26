from django.urls import include, path

import friends.urls
import photos.urls
import posts.urls
import videos.urls

from . import views

app_name = "pages"

urlpatterns = [
    path("<str:username>/", views.PageView.as_view(), name="page"),
    path("<str:username>/edit/", views.EditView.as_view(), name="edit"),

    path('<str:username>/friends/', include(friends.urls, namespace='friends')),
    path('<str:username>/videos/', include(videos.urls, namespace='videos')),
    path('<str:username>/posts/', include(posts.urls, namespace='posts')),
    path('<str:username>/photos/', include(photos.urls, namespace='photos')),
]

