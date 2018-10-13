import os

from Onlyours import settings
from .models import Photo


def delete_unused_photo(sender, **kwargs):
    instance = kwargs["instance"]
    if not sender.objects.filter(photo=instance.photo):
        photo = Photo.objects.get(photo=instance.photo.photo)
        photo.delete()
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.photo.name))
        except FileNotFoundError:
            pass


def delete_photo(sender, **kwargs):
    instance = kwargs["instance"]
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.photo.name))
    except FileNotFoundError:
        pass
