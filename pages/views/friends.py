from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from auth_custom.models import User
from ..models import Friendship, FriendshipRequest


class SendFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest(
                    from_user=request.user, to_user=page_owner
                ).save()
            # it is raised when such FriendshipRequest already exists
            except IntegrityError:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class CancelFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest.objects.get(
                    from_user=request.user, to_user=page_owner
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AcceptFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            friendship_request = FriendshipRequest.objects.filter(
                from_user=page_owner, to_user=request.user
            )
            if friendship_request.exists():
                friendship_request.delete()
                Friendship(user1=request.user, user2=page_owner).save()
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class RefuseFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest.objects.get(
                    from_user=page_owner, to_user=request.user
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class RemoveFriendView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                Friendship.objects.get(
                    Q(user1=page_owner, user2=request.user) |
                    Q(user1=request.user, user2=page_owner)
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)


class FriendsListView(View):
    template_name = "pages/ajax/all_friends.html"

    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = User.objects.get(username=username)
            friends = Friendship.objects.get_friends_of(page_owner)
            session_user_friends = Friendship.objects.get_friends_of(request.user)
            friends.sort(key=lambda e: e.username.lower())
            context = {
                "friends": friends,
                "session_user_friends": session_user_friends
            }
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)
