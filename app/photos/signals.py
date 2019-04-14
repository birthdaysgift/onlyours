import os

from django.conf import settings

from . import models


def delete_unused_photo(sender, **kwargs):
    deleted_posted_photo = kwargs["instance"]
    if not sender.objects.filter(photo=deleted_posted_photo.photo):
        photo = models.Photo.objects.get(file=deleted_posted_photo.photo.file)
        photo.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.file.name))
        except FileNotFoundError:
            pass

        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.thumbnail.name))
        except FileNotFoundError:
            pass
