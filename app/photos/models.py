import os

import PIL.Image
from django.conf import settings
from django.db import models


class Photo(models.Model):
    file = models.ImageField()
    thumbnail = models.ImageField(default='')

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._create_thumbnail()

    def _create_thumbnail(self):
        if not self.thumbnail:
            filename = self.file.name
            photo_path = os.path.join(settings.MEDIA_ROOT, filename)
            img = PIL.Image.open(photo_path)
            img.thumbnail((150, 150))
            thumb_name = 'thumb_' + filename.split('.')[0] + '.jpg'
            thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_name)
            img.save(thumb_path, 'jpeg')
            self.thumbnail = thumb_name
            self.save()


class UserPhoto(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='posted_photos'
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    users_who_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_photos'
    )
    users_who_disliked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='disliked_photos'
    )

    def liked_by(self, user):
        is_liked = self.users_who_liked.filter(id=user.id)
        return is_liked

    def disliked_by(self, user):
        is_disliked = self.users_who_disliked.filter(id=user.id)
        return is_disliked

    def __str__(self):
        return f"{self.user.username}: {self.photo.file.name}"
