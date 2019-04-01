from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from auth_custom.models import User


def add_friend(request, username=None):
    page_owner = get_object_or_404(User, username=username)
    if request.user != page_owner:
        try:
            request.user.friends.add(page_owner)
        except IntegrityError:
            pass
    url = reverse('pages:page', kwargs={'username': username})
    return redirect(url)


def remove_friend(request, username=None):
    page_owner = get_object_or_404(User, username=username)
    if request.user != page_owner:
        request.user.friends.remove(page_owner)
        page_owner.friends.remove(request.user)
    url = reverse('pages:page', kwargs={'username': username})
    return redirect(url)


def all_friends(request, username=None):
    if request.is_ajax():
        page_owner = get_object_or_404(User, username=username)
        friends = page_owner.get_friends(check_common_with=request.user)
        template_name = 'friends/ajax/all_friends.html'
        context = {
            'friends': friends,
        }
        return render(request, template_name, context=context)
