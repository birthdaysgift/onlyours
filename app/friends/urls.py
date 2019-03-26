from django.urls import path

from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.FriendsListView.as_view(), name='all'),
    path('request/send/', views.SendFriendRequestView.as_view(), name='send'),
    path('request/cancel/', views.CancelFriendRequestView.as_view(), name='cancel'),
    path('request/accept/', views.AcceptFriendRequestView.as_view(), name='accept'),
    path('request/refuse/', views.RefuseFriendRequestView.as_view(), name='refuse'),
    path('remove/', views.RemoveFriendView.as_view(), name='remove'),
]
