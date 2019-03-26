import os
import subprocess

from django.db import models

from Onlyours.settings import AUTH_USER_MODEL, MEDIA_ROOT


class Video(models.Model):
    file = models.FileField()
    thumbnail = models.ImageField(default='')

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._create_thumbnail()

    def _create_thumbnail(self):
        if not self.thumbnail:
            filename = self.file.name
            ffmpeg = r'"D:\Program Files\ffmpeg-4.0.2-win64-static\bin\ffmpeg.exe"'
            video = os.path.join(MEDIA_ROOT, filename)
            time = 0.1
            image_name = 'thumb_' + filename.split('.')[0] + '.jpg'
            image = os.path.join(MEDIA_ROOT, image_name)

            cmd = f'{ffmpeg} -i {video} -ss {time} -f image2 -vframes 1 -y -vf scale=200:-2 {image}'
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0:
                video = Video.objects.get(file=filename)
                video.thumbnail = image_name
                video.save()


class UserVideo(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.video.file.name}"


class VideoLike(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    uservideo = models.ForeignKey(UserVideo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} :: {self.uservideo}'


class VideoDislike(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    uservideo = models.ForeignKey(UserVideo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} :: {self.uservideo}'

