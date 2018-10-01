from django.contrib.auth import models as auth_models
from django.db import models


def user_photos_path(instance, filename):
    return f"users/{instance.username}/photos/{filename}"


class User(auth_models.AbstractUser):
    objects = auth_models.UserManager()
    # TODO: avatar delete and default
    avatar = models.ImageField(default="placeholder_avatar.png")
    status = models.CharField(max_length=1000, blank=True, default="")
    city = models.CharField(max_length=50, blank=True, default="")
    birthday = models.DateField(blank=True, null=True, default=None)
    gender = models.CharField(max_length=6, blank=True, default="")
    about = models.TextField(blank=True, default="")
