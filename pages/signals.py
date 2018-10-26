import os

from Onlyours import settings
from .models import Photo, Video


def delete_unused_photo(sender, **kwargs):
    deleted_userphoto = kwargs["instance"]
    if not sender.objects.filter(photo=deleted_userphoto.photo):
        photo = Photo.objects.get(photo=deleted_userphoto.photo.photo)
        photo.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.photo.name))
        except FileNotFoundError:
            pass


def delete_unused_video(sender, **kwargs):
    deleted_uservideo = kwargs["instance"]
    if not sender.objects.filter(video=deleted_uservideo.video):
        video = Video.objects.get(video=deleted_uservideo.video.video)
        video.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, video.video.name))
        except FileNotFoundError:
            pass


def delete_photo(sender, **kwargs):
    deleted_photo = kwargs["instance"]
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, deleted_photo.photo.name))
    except FileNotFoundError:
        pass


def delete_video(sender, **kwargs):
    deleted_video = kwargs["instance"]
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, deleted_video.video.name))
    except FileNotFoundError:
        pass
