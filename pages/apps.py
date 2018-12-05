from django.apps import AppConfig
from django.db.models.signals import post_delete


class PagesConfig(AppConfig):
    name = 'pages'

    def ready(self):
        super().ready()

        from . import signals
        from . import models

        post_delete.connect(
            signals.delete_unused_photo,
            sender=models.UserPhoto
        )

        post_delete.connect(
            signals.delete_unused_video,
            sender=models.UserVideo
        )
