from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename

from auth_custom.models import User

from .forms import AddVideoForm
from .models import UserVideo, Video


def detail_video(request, username=None, uservideo_id=None):
    template_name = 'videos/ajax/detail_video.html'
    if request.is_ajax():
        uservideo = get_object_or_404(UserVideo, id=uservideo_id)

        uservideo.n_likes = uservideo.users_who_liked.count()
        uservideo.n_dislikes = uservideo.users_who_disliked.count()

        uservideo.is_liked = uservideo.liked_by(request.user)
        uservideo.is_disliked = uservideo.disliked_by(request.user)

        context = {'uservideo': uservideo}
        return render(request, template_name, context=context)
    raise Http404()


def all_videos(request, username=None):
    template_name = "videos/ajax/all_videos.html"
    if request.is_ajax():
        page_owner = get_object_or_404(User, username=username)
        user_videos = UserVideo.objects.filter(user=page_owner)
        user_videos = user_videos.select_related("video")
        context = {
            "user_videos": user_videos,
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
        video = get_object_or_404(Video, file=filename)
        user = get_object_or_404(User, username=username)
        UserVideo(user=user, video=video).save()

        kwargs = {'username': username}
    url = reverse('pages:page', kwargs=kwargs)
    return redirect(url)


def delete_video(request, username=None, uservideo_id=None):
    page_owner = get_object_or_404(User, username=username)
    if request.user == page_owner:
        try:
            UserVideo.objects.get(id=uservideo_id).delete()
        except UserVideo.DoesNotExist:
            pass
    url = reverse("pages:page", kwargs={"username": username})
    return redirect(url)


@transaction.atomic
def like_video(request, username=None, uservideo_id=None):
    if request.is_ajax():
        uservideo = get_object_or_404(UserVideo, id=uservideo_id)
        if uservideo.liked_by(request.user):
            uservideo.users_who_liked.remove(request.user)
        else:
            if uservideo.disliked_by(request.user):
                uservideo.users_who_disliked.remove(request.user)
            uservideo.users_who_liked.add(request.user)
        return HttpResponse()
    raise Http404()


@transaction.atomic
def dislike_video(request, username=None, uservideo_id=None):
    if request.is_ajax():
        uservideo = get_object_or_404(UserVideo, id=uservideo_id)
        if uservideo.disliked_by(request.user):
            uservideo.users_who_disliked.remove(request.user)
        else:
            if uservideo.liked_by(request.user):
                uservideo.users_who_liked.remove(request.user)
            uservideo.users_who_disliked.add(request.user)
        return HttpResponse()
    raise Http404()

