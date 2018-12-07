from django.urls import include, path

import pages.views.friends as vfriends
import pages.views.photos as vphotos
import pages.views.videos as vvideos
import pages.views.posts as vposts
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

photos = [
    path('', vphotos.PhotosListView.as_view(), name='photos'),
    path('add/', vphotos.AddPhotoView.as_view(), name='add_photo'),
    path('<int:userphoto_id>/', vphotos.DetailPhotoView.as_view(), name='detail_photo'),
    path('<int:userphoto_id>/delete/', vphotos.DeletePhotoView.as_view(), name='delete_photo'),
    path('<int:userphoto_id>/like/', vphotos.LikePhotoView.as_view(), name='like_photo'),
    path('<int:userphoto_id>/dislike/', vphotos.DislikePhotoView.as_view(), name='dislike_photo'),
]

videos = [
    path('', vvideos.VideosListView.as_view(), name='videos'),
    path('add/', vvideos.AddVideoView.as_view(), name='add_video'),
    path('<int:video_id>/', vvideos.DetailVideoView.as_view(), name='detail_video'),
    path('<int:video_id>/delete/', vvideos.DeleteVideoView.as_view(), name='delete_video'),
]

posts = [
    path('<int:post_id>/delete/', vposts.DeletePostView.as_view(), name='delete_post'),
    path('<int:post_id>/like/', vposts.LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/dislike/', vposts.DislikePostView.as_view(), name='dislike_post')
]

urlpatterns = [
    path("<str:username>/", vpage.PageView.as_view(), name="page"),
    path("<str:username>/edit/", vpage.EditView.as_view(), name="edit"),

    path('<str:username>/friends/', include(friends)),
    path('<str:username>/photos/', include(photos)),
    path('<str:username>/videos/', include(videos)),
    path('<str:username>/posts/', include(posts)),
]

