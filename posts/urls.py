from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete'),
    path('<int:post_id>/like/', views.LikePostView.as_view(), name='like'),
    path('<int:post_id>/dislike/', views.DislikePostView.as_view(), name='dislike'),
    path('get_from_page/<int:page>/', views.GetPostsView.as_view(), name='get_from_page'),
]
