from django.contrib.auth import models as auth_models
from django.db import models


def user_photos_path(instance, filename):
    return f'photos/{instance.username}/{filename}'


class User(auth_models.AbstractUser):
    objects = auth_models.UserManager()
    avatar = models.ImageField(upload_to=user_photos_path, blank=True)
    status = models.CharField(max_length=1000, blank=True, default="")
    city = models.CharField(max_length=50, blank=True, default="")
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1, blank=True, default='',
        choices=(
            ('M', 'Male'),
            ('F', 'Female'),
            ('', '---')
        )
    )
    about = models.TextField(blank=True, default="")
