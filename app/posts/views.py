from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from auth_custom.models import User

from .models import Post, PostDislike, PostLike
from .utils import get_posts_for


class GetPostsView(View):
    template_name = 'posts/posts_list.html'

    def get(self, request, username=None, page=None):
        page_owner = get_object_or_404(User, username=username)
        posts = get_posts_for(page_owner, check_user=request.user, page=page)
        context = {
            'page_owner': page_owner,
            'posts': posts['posts'],
            'next_posts_page': posts['next_posts_page'],
        }
        return render(request, self.template_name, context=context)


class DeletePostView(View):
    template_name = 'posts/ajax/delete_post.html'

    def get(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.is_ajax() and request.user == page_owner:
            post = Post.objects.get(id=post_id)
            return render(request, self.template_name, context={"post": post})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)

    def post(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            Post.objects.get(id=post_id).delete()
        url = reverse('pages:page', kwargs={"username": username})
        return redirect(url)


class LikePostView(View):
    def get(self, request, username=None, post_id=None):
        if request.is_ajax():
            post = Post.objects.get(id=post_id)
            like = PostLike.objects.filter(user=request.user, post=post)
            dislike = PostDislike.objects.filter(user=request.user, post=post)
            if like.exists():
                like[0].delete()
            else:
                if dislike.exists():
                    dislike[0].delete()
                PostLike(user=request.user, post=post).save()
            return HttpResponse()


class DislikePostView(View):
    def get(self, request, username=None, post_id=None):
        if request.is_ajax():
            post = Post.objects.get(id=post_id)
            like = PostLike.objects.filter(user=request.user, post=post)
            dislike = PostDislike.objects.filter(user=request.user, post=post)
            if dislike.exists():
                dislike[0].delete()
            else:
                if like.exists():
                    like[0].delete()
                PostDislike(user=request.user, post=post).save()
            return HttpResponse()
