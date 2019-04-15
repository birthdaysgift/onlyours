from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename

from auth_custom.models import User

from .forms import AddVideoForm
from .models import UserVideo, Video, VideoDislike, VideoLike


def detail_video(request, username=None, uservideo_id=None):
    template_name = 'videos/ajax/detail_video.html'
    if request.is_ajax():
        uservideo = get_object_or_404(UserVideo, id=uservideo_id)
        likes = VideoLike.objects.filter(uservideo=uservideo)
        dislikes = VideoDislike.objects.filter(uservideo=uservideo)
        setattr(uservideo, 'likes', likes)
        setattr(uservideo, 'dislikes', dislikes)
        is_liked = VideoLike.objects.filter(
            uservideo=uservideo, user=request.user
        ).exists()
        is_disliked = VideoDislike.objects.filter(
            uservideo=uservideo, user=request.user
        ).exists()
        setattr(uservideo, 'is_liked', is_liked)
        setattr(uservideo, 'is_disliked', is_disliked)
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
        like = VideoLike.objects.filter(
            user=request.user, uservideo=uservideo
        )
        dislike = VideoDislike.objects.filter(
            user=request.user, uservideo=uservideo
        )
        if like.exists():
            like[0].delete()
        else:
            if dislike.exists():
                dislike[0].delete()
            VideoLike(user=request.user, uservideo=uservideo).save()
        return HttpResponse()
    raise Http404()


@transaction.atomic
def dislike_video(request, username=None, uservideo_id=None):
    if request.is_ajax():
        uservideo = get_object_or_404(UserVideo, id=uservideo_id)
        like = VideoLike.objects.filter(
            user=request.user, uservideo=uservideo
        )
        dislike = VideoDislike.objects.filter(
            user=request.user, uservideo=uservideo
        )
        if dislike.exists():
            dislike[0].delete()
        else:
            if like.exists():
                like[0].delete()
            VideoDislike(user=request.user, uservideo=uservideo).save()
        return HttpResponse()
    raise Http404()
