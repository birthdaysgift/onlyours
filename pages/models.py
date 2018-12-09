import os
import subprocess

from django.db import models
from django.db.models import Q
import PIL

from auth_custom.models import User
from Onlyours.settings import AUTH_USER_MODEL, MEDIA_ROOT


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


class FriendshipManager(models.Manager):

    def get_friends_of(self, user, order_by=None):
        user_friend_pairs = self.all().filter(
            Q(user1=user) | Q(user2=user)
        )
        user_friend_pairs = user_friend_pairs.select_related("user1", "user2")
        if order_by:
            user_friend_pairs = user_friend_pairs.order_by(order_by)
        friends = []
        for pair in user_friend_pairs:
            if pair.user1 == user:
                friends.append(pair.user2)
            else:
                friends.append(pair.user1)
        return friends


class Friendship(models.Model):
    objects = FriendshipManager()

    user1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="user1")
    user2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="user2")

    def __str__(self):
        return f'{self.user1} <-> {self.user2}'


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="to_user")

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'

    class Meta:
        unique_together = ("from_user", "to_user")