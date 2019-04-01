from django.urls import path

from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.all_friends, name='all'),
    path('add/', views.add_friend, name='add'),
    path('remove/', views.remove_friend, name='remove'),
]
