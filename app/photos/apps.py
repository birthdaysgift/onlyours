from django.apps import AppConfig
from django.db.models.signals import post_delete


class PhotosConfig(AppConfig):
    name = 'photos'

    def ready(self):
        super().ready()

        from . import signals
        from . import models

        post_delete.connect(
            signals.delete_posted_photo,
            sender=models.PostedPhoto
        )
        post_delete.connect(
            signals.delete_photo,
            sender=models.Photo
        )
