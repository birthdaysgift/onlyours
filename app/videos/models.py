import os
import subprocess

from django.conf import settings
from django.db import models


class Video(models.Model):
    file = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='videos', blank=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._create_thumbnail()

    def _create_thumbnail(self):
        if not self.thumbnail:
            filename = self.file.name
            ffmpeg = r'"D:\Program Files\ffmpeg-4.0.2-win64-static\bin\ffmpeg.exe"'
            video_path = os.path.join(settings.MEDIA_ROOT, filename)
            time = 0.1
            path_before, slash, filename = filename.rpartition('/')
            filename, extension = filename.split('.')
            thumb_name = ''.join((
                path_before, slash, 'thumb_', filename, '.', extension
            ))
            thumb_abspath = os.path.join(settings.MEDIA_ROOT, thumb_name)

            cmd = f'{ffmpeg} -i {video_path} -ss {time} -f image2 -vframes 1 -y -vf scale=200:-2 {thumb_abspath}'
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0:
                video = Video.objects.get(file=filename)
                video.thumbnail = thumb_name
                video.save()


class PostedVideo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='posted_videos'
    )
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    users_who_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_videos'
    )
    users_who_disliked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='disliked_videos'
    )

    def liked_by(self, user):
        is_liked = self.users_who_liked.filter(id=user.id)
        return is_liked

    def disliked_by(self, user):
        is_disliked = self.users_who_disliked.filter(id=user.id)
        return is_disliked

    def __str__(self):
        return f"{self.user.username}: {self.video.file.name}"
