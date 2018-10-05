import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from auth_custom.models import User

from .forms import EditPageForm
from .models import Friendship, FriendshipRequest


def get_friends_of(user):
    user_friend_pairs = Friendship.objects.filter(
                Q(user1=user) | Q(user2=user)
            ).select_related("user1", "user2")
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
                "user": user,
                "current_user": request.user,
                "friends": friends,
                "friendship_status": friendship_status
            }
            return render(request, self.template_name, context=context)


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


class ResetFriendRequestView(View):
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
