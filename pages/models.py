import os
import subprocess

from django.db import models
import PIL

from auth_custom.models import User
from Onlyours.settings import AUTH_USER_MODEL, MEDIA_ROOT


class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               default=0, related_name="post_sender")
    receiver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                 default=0, related_name="post_receiver")
    text = models.TextField()


class Photo(models.Model):
    file = models.ImageField()
    thumbnail = models.ImageField(default='')

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super().save()
        self._create_thumbnail()

    def _create_thumbnail(self):
        if not self.thumbnail:
            filename = self.file.name
            photo_path = os.path.join(MEDIA_ROOT, filename)
            img = PIL.Image.open(photo_path)
            img.thumbnail((150, 150))
            thumb_name = 'thumb_' + filename.split('.')[0] + '.jpg'
            thumb_path = os.path.join(MEDIA_ROOT, thumb_name)
            img.save(thumb_path, 'jpeg')
            self.thumbnail = thumb_name
            self.save()


class UserPhoto(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.photo.file.name}"


class Video(models.Model):
    file = models.FileField()
    thumbnail = models.ImageField(default='')

    def __str__(self):
        return self.file.name

    def save(self):
        super().save()
        self._create_thumbnail()

    def _create_thumbnail(self):
        if not self.thumbnail:
            filename = self.file.name
            ffmpeg = r'"D:\Program Files\ffmpeg-4.0.2-win64-static\bin\ffmpeg.exe"'
            video = os.path.join(MEDIA_ROOT, filename)
            time = 0.1
            size = '100x100'
            image_name = 'thumb_' + filename.split('.')[0] + '.jpg'
            image = os.path.join(MEDIA_ROOT, image_name)

            cmd = f'{ffmpeg} -i {video} -ss {time} -f image2 -vframes 1 -y -s {size} {image}'
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


class Friendship(models.Model):
    user1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="user1")
    user2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="user2")


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="to_user")

    class Meta:
        unique_together = ("from_user", "to_user")