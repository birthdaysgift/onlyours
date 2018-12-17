from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from auth_custom.models import User

from .models import Post, PostDislike, PostLike


class GetPostsView(View):
    template_name = 'posts/ajax/posts.html'

    def get(self, request, username=None, page=None):
        # get page owner
        page_owner = get_object_or_404(User, username=username)

        # get posts and likes/dislikes for them
        posts = Post.objects.filter(receiver=page_owner)
        posts = posts.select_related('sender')
        posts = posts.order_by("-date", "-time")
        paginator = Paginator(posts, per_page=10)
        try:
            posts_page = paginator.get_page(page)
        except InvalidPage:
            raise Http404(f'Posts page `{page}` does not exists.')
        posts = posts_page.object_list
        posts.attach_likes(check_user=request.user)
        if posts_page.has_next():
            next_posts_page = posts_page.next_page_number()
        else:
            next_posts_page = None
        context = {
            'page_owner': page_owner,
            'posts': posts,
            'next_posts_page': next_posts_page,
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
