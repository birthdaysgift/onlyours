from django.urls import path

from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.all_videos, name='all'),
    path('add/', views.add_video, name='add'),
    path('<int:posted_video_id>/', views.detail_video, name='detail'),
    path('<int:posted_video_id>/delete/', views.delete_video, name='delete'),
    path('<int:posted_video_id>/like/', views.like_video, name='like'),
    path('<int:posted_video_id>/dislike/', views.dislike_video, name='dislike')
]

