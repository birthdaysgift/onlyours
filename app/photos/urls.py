from django.urls import path

from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.all_photos, name='all'),
    path('add/', views.add_photo, name='add'),
    path('<int:posted_photo_id>/', views.detail_photo, name='detail'),
    path('<int:posted_photo_id>/delete/', views.delete_photo, name='delete'),
    path('<int:posted_photo_id>/like/', views.like_photo, name='like'),
    path('<int:posted_photo_id>/dislike/', views.dislike_photo, name='dislike'),
]
