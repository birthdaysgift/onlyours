from django.urls import include, path

import photos.urls
import posts.urls
import videos.urls

import pages.views.friends as vfriends
import pages.views.page as vpage

app_name = "pages"

friends = [
    path('', vfriends.FriendsListView.as_view(), name='friends'),
    path('send/', vfriends.SendFriendRequestView.as_view(), name='send_friend_request'),
    path('cancel/', vfriends.CancelFriendRequestView.as_view(), name='cancel_friend_request'),
    path('accept/', vfriends.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('refuse/', vfriends.RefuseFriendRequestView.as_view(), name='refuse_friend_request'),
    path('remove/', vfriends.RemoveFriendView.as_view(), name='remove_friend'),
]

urlpatterns = [
    path("<str:username>/", vpage.PageView.as_view(), name="page"),
    path("<str:username>/edit/", vpage.EditView.as_view(), name="edit"),

    path('<str:username>/friends/', include(friends)),
    path('<str:username>/videos/', include(videos.urls, namespace='videos')),
    path('<str:username>/posts/', include(posts.urls, namespace='posts')),
    path('<str:username>/photos/', include(photos.urls, namespace='photos')),
]

