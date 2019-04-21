from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from auth_custom.models import User
from posts.models import Post, get_posts_for
from posts.forms import AddPostForm
from videos.models import PostedVideo

from .forms import EditPageForm


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")
    template_name = "pages/base.html"

    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)

        posts = get_posts_for(
            page_owner, count_likes=True, check_user=request.user
        )

        posted_photos = page_owner.get_posted_photos()[:6]

        # get posted_videos
        posted_videos = PostedVideo.objects.filter(user=page_owner)
        posted_videos = posted_videos.select_related("user", "video")[:6]

        friends = page_owner.get_friends()
        if friends:
            friends = friends.order_by('?')[:6]

        page_owner.sent_friend_request = page_owner.sent_friend_request_to(
            request.user
        )
        request.user.sent_friend_request = request.user.sent_friend_request_to(
            page_owner
        )

        context = {
            "form": AddPostForm(),
            "page_owner": page_owner,
            "posts": posts,
            "friends": friends,
            "posted_photos": posted_photos,
            "posted_videos": posted_videos,
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
