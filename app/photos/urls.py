from django.urls import path

from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.PhotosListView.as_view(), name='all'),
    path('add/', views.AddPhotoView.as_view(), name='add'),
    path('<int:posted_photo_id>/', views.DetailPhotoView.as_view(), name='detail'),
    path('<int:posted_photo_id>/delete/', views.DeletePhotoView.as_view(), name='delete'),
    path('<int:posted_photo_id>/like/', views.like_photo, name='like'),
    path('<int:posted_photo_id>/dislike/', views.dislike_photo, name='dislike'),
]
