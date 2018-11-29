import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.text import get_valid_filename
from django.views import View

from auth_custom.models import User
from .forms import EditPageForm, AddPostForm, AddPhotoForm, AddVideoForm
from .models import Friendship, FriendshipRequest, Post, UserPhoto, Photo, \
    UserVideo, Video


def get_friends_of(user, order_by=None):
    user_friend_pairs = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).select_related("user1", "user2")
    if order_by:
        user_friend_pairs = user_friend_pairs.order_by(order_by)
    friends = []
    for pair in user_friend_pairs:
        if pair.user1 == user:
            friends.append(pair.user2)
        else:
            friends.append(pair.user1)
    return friends


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")
    template_name = "pages/base.html"

    def get(self, request, username=None):
        # get page owner
        page_owner = get_object_or_404(User, username=username)

        # get posts
        posts = Post.objects.filter(receiver=page_owner)
        posts = posts.select_related('sender')
        posts = posts.order_by("-date", "-time")

        # get user_photos
        user_photos = UserPhoto.objects.filter(user=page_owner)
        user_photos = user_photos.select_related("user", "photo")[:6]

        # get user_videos
        user_videos = UserVideo.objects.filter(user=page_owner)
        user_videos = user_videos.select_related("user", "video")[:6]

        # get friends
        friends = get_friends_of(page_owner)
        max_friends = 6  # max friends on friends-panel in page.html
        if len(friends) < max_friends:
            friends = random.sample(friends, len(friends))
        else:
            friends = random.sample(friends, max_friends)

        # get friendship status
        # friend:     user <-> page_owner
        # requested:  user --> page_owner
        # requesting: user <-- page_owner
        friendship_status = None
        if request.user in friends:
            friendship_status = "friend"
        requested = FriendshipRequest.objects.filter(
            from_user=request.user, to_user=page_owner
        ).exists()
        if requested:
            friendship_status = "requested"
        requesting = FriendshipRequest.objects.filter(
            from_user=page_owner, to_user=request.user
        ).exists()
        if requesting:
            friendship_status = "requesting"

        context = {
            "form": AddPostForm(),
            "page_owner": page_owner,
            "posts": posts,
            "friends": friends,
            "user_photos": user_photos,
            "friendship_status": friendship_status,
            "user_videos": user_videos
        }
        return render(request, self.template_name, context=context)

    def post(self, request, username=None):
        form = AddPostForm(request.POST)
        if form.is_valid():
            receiver = get_object_or_404(User, username=username)
            Post(
                sender=request.user,
                receiver=receiver,
                text=form.cleaned_data["text"]
            ).save()
            url = reverse('pages:page', kwargs={'username': username})
            return redirect(url)
        else:
            return render(request, self.template_name, context={"form": form})


class DeletePostView(View):
    template_name = 'pages/ajax/delete_post.html'

    def get(self, request, username=None, post_id=None):
        post = Post.objects.get(id=post_id)
        return render(request, self.template_name, context={"post": post})

    def post(self, request, username=None, post_id=None):
        Post.objects.get(id=post_id).delete()
        return redirect(reverse('pages:page', kwargs={"username": username}))


class EditView(LoginRequiredMixin, View):
    template_name = "pages/edit.html"

    def get(self, request, username=None):
        if username != request.user.username:
            return redirect(reverse_lazy(
                "pages:edit",
                kwargs={"username": request.user.username}
            ))
        return render(request, self.template_name, context={
            "form": EditPageForm(instance=request.user)
        })

    def post(self, request, username=None):
        form = EditPageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("pages:page", kwargs={
                "username": request.user.username
            }))
        return render(request, self.template_name, context={"form": form})


class SendFriendRequestView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        FriendshipRequest(from_user=request.user, to_user=user).save()
        return redirect(reverse("pages:page", kwargs={
            "username": username
        }))


class CancelFriendRequestView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        FriendshipRequest.objects.get(
            from_user=request.user, to_user=user
        ).delete()
        return redirect(reverse("pages:page", kwargs={
            "username": username
        }))


class AcceptFriendRequestView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        friendship_request = FriendshipRequest.objects.filter(
            from_user=user, to_user=request.user
        )
        if friendship_request.exists():
            friendship_request.delete()
            Friendship(user1=request.user, user2=user).save()
            return redirect(reverse("pages:page", kwargs={
                "username": username
            }))


class DenyFriendRequestView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        FriendshipRequest.objects.get(
            from_user=user, to_user=request.user
        ).delete()
        return redirect(reverse("pages:page", kwargs={
            "username": username
        }))


class RemoveFriendView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        Friendship.objects.get(
            Q(user1=user, user2=request.user) |
            Q(user1=request.user, user2=user)
        ).delete()
        return redirect(reverse("pages:page", kwargs={
            "username": username
        }))


class FriendsListView(View):
    def get(self, request, username=None):
        page_owner = User.objects.get(username=username)
        friends = get_friends_of(page_owner)
        session_user_friends = get_friends_of(request.user)
        friends.sort(key=lambda e: e.username.lower())
        return render(request, "pages/ajax/all_friends.html",
                      context={"friends": friends,
                               "session_user_friends": session_user_friends})


class PhotosListView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        user_photos = UserPhoto.objects.filter(user=page_owner)
        user_photos = user_photos.select_related('photo')
        return render(request, "pages/ajax/all_photos.html", context={
            "user_photos": user_photos,
            "page_owner": page_owner,
            "photo_form": AddPhotoForm()
        })


class AddNewPhotoView(View):
    template_name = 'pages/ajax/all_photos.html'

    def post(self, request, username=None):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=username)
            filename = get_valid_filename(form.cleaned_data['file'].name)
            photo = get_object_or_404(
                Photo,
                file=filename
            )
            UserPhoto(user=user, photo=photo).save()
            return redirect(reverse("pages:page", kwargs={
                "username": username
            }))
        else:
            return render(request, self.template_name, context={
                "form": form
            })


class DeletePhotoView(View):
    def get(self, request, username=None, userphoto_id=None):
        UserPhoto.objects.get(id=userphoto_id).delete()
        return redirect(reverse("pages:page", kwargs={"username": username}))


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


class VideosListView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        user_videos = UserVideo.objects.filter(user=page_owner)
        user_videos = user_videos.select_related("video")
        return render(request, "pages/ajax/all_videos.html", context={
            "user_videos": user_videos,
            "page_owner": page_owner,
            "video_form": AddVideoForm()
        })


class AddNewVideoView(View):
    template_name = "pages/ajax/add_video.html"

    def get(self, request, username=None):
        return render(request, self.template_name, context={
            "form": AddVideoForm()
        })

    def post(self, request, username=None):
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=username)
            filename = get_valid_filename(form.cleaned_data['file'].name)
            video = get_object_or_404(
                Video,
                file=filename
            )
            UserVideo(user=user, video=video).save()
            return redirect(reverse("pages:page", kwargs={
                "username": username
            }))
        else:
            return render(request, self.template_name, context={
                "form": form
            })


class DeleteVideoView(View):
    def get(self, request, username=None, uservideo=None):
        UserVideo.objects.get(id=uservideo).delete()
        return redirect(reverse("pages:page", kwargs={"username": username}))
