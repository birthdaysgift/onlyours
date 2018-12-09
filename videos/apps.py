from django.apps import AppConfig
from django.db.models.signals import post_delete


class VideosConfig(AppConfig):
    name = 'videos'

    def ready(self):
        super().ready()

        from . import signals
        from . import models

        post_delete.connect(
            signals.delete_unused_video,
            sender=models.UserVideo
        )
