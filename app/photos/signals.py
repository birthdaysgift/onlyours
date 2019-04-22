import os

from django.conf import settings

from . import models


def delete_posted_photo(sender, **kwargs):
    deleted_posted_photo = kwargs["instance"]
    if not sender.objects.filter(photo=deleted_posted_photo.photo):
        photo = models.Photo.objects.get(file=deleted_posted_photo.photo.file)
        photo.delete()


def delete_photo(sender, **kwargs):
    deleted_photo = kwargs['instance']
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, deleted_photo.file.name))
    except FileNotFoundError:
        pass
    if deleted_photo.thumbnail:
        try:
            os.remove(os.path.join(
                settings.MEDIA_ROOT, deleted_photo.thumbnail.name
            ))
        except FileNotFoundError:
            pass
