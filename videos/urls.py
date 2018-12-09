from django.urls import path

from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideosListView.as_view(), name='all'),
    path('add/', views.AddVideoView.as_view(), name='add'),
    path('<int:uservideo_id>/', views.DetailVideoView.as_view(), name='detail'),
    path('<int:uservideo_id>/delete/', views.DeleteVideoView.as_view(), name='delete'),
    path('<int:uservideo_id>/like/', views.LikeVideoView.as_view(), name='like'),
    path('<int:uservideo_id>/dislike/', views.DislikeVideoView.as_view(), name='dislike')
]

