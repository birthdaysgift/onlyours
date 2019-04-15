from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from auth_custom.models import User

from .models import get_posts_for, Post


def all_posts(request, username=None, page=None):
    template_name = 'posts/posts_list.html'
    page_owner = get_object_or_404(User, username=username)
    posts = get_posts_for(
        page_owner, page=page, count_likes=True, check_user=request.user
    )
    context = {
        'page_owner': page_owner,
        'posts': posts,
    }
    return render(request, template_name, context=context)


class DeletePostView(View):
    template_name = 'posts/ajax/delete_post.html'

    def get(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.is_ajax() and request.user == page_owner:
            post = Post.objects.get(id=post_id)
            return render(request, self.template_name, context={"post": post})
        raise Http404()

    def post(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            Post.objects.get(id=post_id).delete()
        url = reverse('pages:page', kwargs={"username": username})
        return redirect(url)


@transaction.atomic
def like_post(request, username=None, post_id=None):
    if request.method == 'GET' and request.is_ajax():
        post = get_object_or_404(Post, id=post_id)
        if post.disliked_by(request.user):
            post.users_who_disliked.remove(request.user)
        if post.liked_by(request.user):
            post.users_who_liked.remove(request.user)
        else:
            post.users_who_liked.add(request.user)
        post.save()
    raise Http404()


@transaction.atomic
def dislike_post(request, username=None, post_id=None):
    if request.method == 'GET' and request.is_ajax():
        post = Post.objects.get(id=post_id)
        if post.liked_by(request.user):
            post.users_who_liked.remove(request.user)
        if post.disliked_by(request.user):
            post.users_who_disliked.remove(request.user)
        else:
            post.users_who_disliked.add(request.user)
        post.save()
    raise Http404()
