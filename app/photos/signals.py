import os

from Onlyours.settings import MEDIA_ROOT
from . import models


def delete_unused_photo(sender, **kwargs):
    deleted_userphoto = kwargs["instance"]
    if not sender.objects.filter(photo=deleted_userphoto.photo):
        photo = models.Photo.objects.get(file=deleted_userphoto.photo.file)
        photo.delete()
        try:
            os.remove(os.path.join(MEDIA_ROOT, photo.file.name))
        except FileNotFoundError:
            pass

        try:
            os.remove(os.path.join(MEDIA_ROOT, photo.thumbnail.name))
        except FileNotFoundError:
            pass
