import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View


from auth_custom.models import User
from friends.models import Friendship, FriendshipRequest
from photos.models import UserPhoto
from posts.models import Post, PostDislike, PostLike
from posts.forms import AddPostForm
from videos.models import UserVideo

from .forms import EditPageForm


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")
    template_name = "pages/base.html"

    def get(self, request, username=None):
        # get page owner
        page_owner = get_object_or_404(User, username=username)

        # get posts and likes/dislikes for them
        posts = Post.objects.filter(receiver=page_owner)
        posts = posts.select_related('sender')
        posts = posts.order_by("-date", "-time")
        for post in posts:
            likes = PostLike.objects.filter(post=post)
            likes = likes.select_related('user')
            dislikes = PostDislike.objects.filter(post=post)
            dislikes = dislikes.select_related('user')
            setattr(post, 'likes', likes)
            setattr(post, 'dislikes', dislikes)
            is_liked = PostLike.objects.filter(
                post=post, user=request.user
            ).exists()
            is_disliked = PostDislike.objects.filter(
                post=post, user=request.user
            ).exists()
            setattr(post, 'is_liked', is_liked)
            setattr(post, 'is_disliked', is_disliked)

        # get user_photos
        user_photos = UserPhoto.objects.filter(user=page_owner)
        user_photos = user_photos.select_related("user", "photo")[:6]

        # get user_videos
        user_videos = UserVideo.objects.filter(user=page_owner)
        user_videos = user_videos.select_related("user", "video")[:6]

        # get friends
        friends = Friendship.objects.get_friends_of(page_owner)
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


class EditView(LoginRequiredMixin, View):
    template_name = "pages/edit.html"

    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            form = EditPageForm(instance=request.user)
            return render(request, self.template_name, context={"form": form})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)

    def post(self, request, username=None):
        form = EditPageForm(request.POST, request.FILES, instance=request.user)
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            if form.is_valid():
                form.save()
                kwargs = {"username": request.user.username}
                url = reverse('pages:page', kwargs=kwargs)
                return redirect(url)
            return render(request, self.template_name, context={"form": form})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)
