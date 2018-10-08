import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from auth_custom.models import User

from .forms import EditPageForm, AddPostForm
from .models import Friendship, FriendshipRequest, Post


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
            friends = get_friends_of(user)
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
                "friendship_status": friendship_status
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
        return render(request, "pages/friends.html",
                      context={"friends": friends,
                               "session_user_friends": session_user_friends})
