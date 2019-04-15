from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete'),
    path('<int:post_id>/like/', views.like_post, name='like'),
    path('<int:post_id>/dislike/', views.dislike_post, name='dislike'),
    path('get_from_page/<int:page>/', views.all_posts, name='get_from_page'),
]
