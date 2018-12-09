import os

from Onlyours.settings import MEDIA_ROOT
from .models import Video


def delete_unused_video(sender, **kwargs):
    deleted_uservideo = kwargs["instance"]
    if not sender.objects.filter(video=deleted_uservideo.video):
        video = Video.objects.get(file=deleted_uservideo.video.file)
        video.delete()
        try:
            os.remove(os.path.join(MEDIA_ROOT, video.file.name))
        except FileNotFoundError:
            pass
        try:
            os.remove(os.path.join(MEDIA_ROOT, video.thumbnail.name))
        except FileNotFoundError:
            pass
