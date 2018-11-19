import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
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

    template_name = "pages/page.html"

    def get(self, request, username=None):
        if username is not None:
            user = get_object_or_404(User, username=username)
            posts = Post.objects.filter(receiver=user).select_related("sender")
            posts = posts.order_by("-date", "-time")
            friends = get_friends_of(user)
            photos = UserPhoto.objects.filter(user=user)
            photos = photos.select_related("user", "photo")[:6]
            videos = UserVideo.objects.filter(user=user)
            videos = videos.select_related("user", "video")[:6]
            friendship_status = None
            if request.user in friends:
                friendship_status = "friend"
            requesting = FriendshipRequest.objects.filter(
                    from_user=user, to_user=request.user
            ).exists()
            if requesting:
                friendship_status = "requesting"
            requested = FriendshipRequest.objects.filter(
                from_user=request.user, to_user=user
            ).exists()
            if requested:
                friendship_status = "requested"
            k = 6
            if len(friends) < k:
                k = len(friends)
            friends = random.sample(friends, k)
            context = {
                "form": AddPostForm(),
                "user": user,
                "current_user": request.user,
                "posts": posts,
                "friends": friends,
                "photos": photos,
                "friendship_status": friendship_status,
                "videos": videos
            }
            return render(request, self.template_name, context=context)

    def post(self, request, username=None):
        form = AddPostForm(request.POST)
        if form.is_valid():
            Post(
                sender=request.user,
                receiver=get_object_or_404(User, username=username),
                text=form.cleaned_data["text"]
            ).save()
            return redirect(reverse("pages:page", kwargs={
                "username": username}))
        else:
            return render(request, self.template_name, context={"form": form})


class PostDeleteConfirmView(View):
    def get(self, request, username=None, post_id=None):
        post = Post.objects.get(id=post_id)
        return render(request, 'pages/delete_post.html', context={"post": post})


class DeletePostView(View):
    def get(self, request, username=None, post_id=None):
        Post.objects.get(id=post_id).delete()
        return redirect(reverse('pages:page', kwargs={
            "username": username
        }))


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
        user = User.objects.get(username=username)
        friends = get_friends_of(user)
        session_user_friends = get_friends_of(request.user)
        # TODO: make sort in db query
        friends.sort(key=lambda e: e.username.lower())
        return render(request, "pages/all_friends.html",
                      context={"friends": friends,
                               "session_user_friends": session_user_friends})


class PhotosListView(View):
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        photos = UserPhoto.objects.filter(user=user).select_related("photo")
        return render(request, "pages/all_photos.html", context={
            "photos": photos,
            "user": user,
            "photo_form": AddPhotoForm(),
            "current_user": request.user
        })


class AddNewPhotoView(View):
    template_name = 'pages/all_photos.html'

    def post(self, request, username=None):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=username)
            # TODO: clarify name formatting when saving to db
            photo = get_object_or_404(
                Photo,
                photo=form.cleaned_data['photo'].name.strip().replace(" ", "_")
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
        user = get_object_or_404(User, username=username)
        videos = UserVideo.objects.filter(user=user).select_related("video")
        return render(request, "pages/all_videos.html", context={
            "videos": videos,
            "user": user,
            "video_form": AddVideoForm(),
            "current_user": request.user
        })


class AddNewVideoView(View):
    template_name = "pages/add_video.html"

    def get(self, request, username=None):
        return render(request, self.template_name, context={
            "form": AddVideoForm()
        })

    def post(self, request, username=None):
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=username)
            # TODO: clarify name formatting when saving to db
            video = get_object_or_404(
                Video,
                video=form.cleaned_data['video'].name.strip().replace(' ', '_')
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
