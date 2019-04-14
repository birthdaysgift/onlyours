import os

from django.conf import settings

from .models import Video


def delete_unused_video(sender, **kwargs):
    deleted_uservideo = kwargs["instance"]
    if not sender.objects.filter(video=deleted_uservideo.video):
        video = Video.objects.get(file=deleted_uservideo.video.file)
        video.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, video.file.name))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, video.thumbnail.name))
        except FileNotFoundError:
            pass