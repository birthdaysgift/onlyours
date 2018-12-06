from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views import View

from auth_custom.models import User
from ..forms import AddVideoForm
from ..models import UserVideo, Video


class DetailVideoView(View):
    template_name = 'pages/ajax/detail_video.html'

    def get(self, request, username=None, video_id=None):
        if request.is_ajax():
            video = get_object_or_404(Video, id=video_id)
            return render(request, self.template_name, context={'video': video})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class VideosListView(View):
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
            return render(request, "pages/ajax/all_videos.html", context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AddVideoView(View):
    template_name = "pages/ajax/add_video.html"

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
    def get(self, request, username=None, uservideo=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                UserVideo.objects.get(id=uservideo).delete()
            except UserVideo.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)
