from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views import View

from auth_custom.models import User

from .forms import AddVideoForm
from .models import UserVideo, Video, VideoDislike, VideoLike


class DetailVideoView(View):
    template_name = 'videos/ajax/detail_video.html'

    def get(self, request, username=None, uservideo_id=None):
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
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class VideosListView(View):
    template_name = "videos/ajax/all_videos.html"

    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = get_object_or_404(User, username=username)
            user_videos = UserVideo.objects.filter(user=page_owner)
            user_videos = user_videos.select_related("video")
            context = {
                "user_videos": user_videos,
                "page_owner": page_owner,
                "video_form": AddVideoForm()
            }
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AddVideoView(View):
    template_name = "videos/ajax/add_video.html"

    def post(self, request, username=None):
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


class DeleteVideoView(View):
    def get(self, request, username=None, uservideo_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                UserVideo.objects.get(id=uservideo_id).delete()
            except UserVideo.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)


class LikeVideoView(View):
    def get(self, request, username=None, uservideo_id=None):
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


class DislikeVideoView(View):
    def get(self, request, username=None, uservideo_id=None):
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
