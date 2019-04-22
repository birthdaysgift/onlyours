from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename

from auth_custom.models import User

from .forms import AddVideoForm
from .models import PostedVideo, Video


def detail_video(request, username=None, posted_video_id=None):
    template_name = 'videos/ajax/detail_video.html'
    if request.is_ajax():
        posted_video = get_object_or_404(PostedVideo, id=posted_video_id)

        posted_video.n_likes = posted_video.users_who_liked.count()
        posted_video.n_dislikes = posted_video.users_who_disliked.count()

        posted_video.is_liked = posted_video.liked_by(request.user)
        posted_video.is_disliked = posted_video.disliked_by(request.user)

        context = {'posted_video': posted_video}
        return render(request, template_name, context=context)
    raise Http404()


def all_videos(request, username=None):
    template_name = "videos/ajax/all_videos.html"
    if request.is_ajax():
        page_owner = get_object_or_404(User, username=username)
        posted_videos = page_owner.get_posted_videos()
        context = {
            "posted_videos": posted_videos,
            "page_owner": page_owner,
            "video_form": AddVideoForm()
        }
        return render(request, template_name, context=context)
    raise Http404()


def add_video(request, username=None):
    template_name = "videos/ajax/add_video.html"
    page_owner = get_object_or_404(User, username=username)
    form = AddVideoForm(request.POST, request.FILES)
    if request.user == page_owner and form.is_valid():
        form.save()

        filename = get_valid_filename(form.cleaned_data['file'].name)
        video = get_object_or_404(Video, file='videos/'+filename)
        user = get_object_or_404(User, username=username)
        PostedVideo(user=user, video=video).save()

        kwargs = {'username': username}
    url = reverse('pages:page', kwargs=kwargs)
    return redirect(url)


def delete_video(request, username=None, posted_video_id=None):
    page_owner = get_object_or_404(User, username=username)
    if request.user == page_owner:
        try:
            PostedVideo.objects.get(id=posted_video_id).delete()
        except PostedVideo.DoesNotExist:
            pass
    url = reverse("pages:page", kwargs={"username": username})
    return redirect(url)


@transaction.atomic
def like_video(request, username=None, posted_video_id=None):
    if request.is_ajax():
        posted_video = get_object_or_404(PostedVideo, id=posted_video_id)
        if posted_video.liked_by(request.user):
            posted_video.users_who_liked.remove(request.user)
        else:
            if posted_video.disliked_by(request.user):
                posted_video.users_who_disliked.remove(request.user)
            posted_video.users_who_liked.add(request.user)
        return HttpResponse()
    raise Http404()


@transaction.atomic
def dislike_video(request, username=None, posted_video_id=None):
    if request.is_ajax():
        posted_video = get_object_or_404(PostedVideo, id=posted_video_id)
        if posted_video.disliked_by(request.user):
            posted_video.users_who_disliked.remove(request.user)
        else:
            if posted_video.liked_by(request.user):
                posted_video.users_who_liked.remove(request.user)
            posted_video.users_who_disliked.add(request.user)
        return HttpResponse()
    raise Http404()

