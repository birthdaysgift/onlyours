from django.urls import path

from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.PhotosListView.as_view(), name='all'),
    path('add/', views.AddPhotoView.as_view(), name='add'),
    path('<int:userphoto_id>/', views.DetailPhotoView.as_view(), name='detail'),
    path('<int:userphoto_id>/delete/', views.DeletePhotoView.as_view(), name='delete'),
    path('<int:userphoto_id>/like/', views.like_photo, name='like'),
    path('<int:userphoto_id>/dislike/', views.dislike_photo, name='dislike'),
]
