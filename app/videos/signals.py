import os

from django.conf import settings

from .models import Video


def delete_unused_video(sender, **kwargs):
    deleted_posted_video = kwargs["instance"]
    if not sender.objects.filter(video=deleted_posted_video.video):
        video = Video.objects.get(file=deleted_posted_video.video.file)
        video.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, video.file.name))
        except FileNotFoundError:
            pass
        if video.thumbnail:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, video.thumbnail.name))
            except FileNotFoundError:
                pass
