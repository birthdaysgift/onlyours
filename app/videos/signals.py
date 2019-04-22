import os

from django.conf import settings

from .models import Video


def delete_posted_video(sender, **kwargs):
    deleted_posted_video = kwargs["instance"]
    if not sender.objects.filter(video=deleted_posted_video.video):
        video = Video.objects.get(file=deleted_posted_video.video.file)
        video.delete()


def delete_video(sender, **kwargs):
    deleted_video = kwargs['instance']
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, deleted_video.file.name))
    except FileNotFoundError:
        pass
    if deleted_video.thumbnail:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, deleted_video.thumbnail.name))
        except FileNotFoundError:
            pass
