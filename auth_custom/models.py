from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    objects = auth_models.UserManager()

    avatar = models.URLField(default="https://i2.bongacams.com/00d/"
                                     "0e8/134/60307272da340d6aeccaf1"
                                     "09399d57a2_thumb_big.jpg")
    status = models.CharField(max_length=1000, blank=True, default="")
    city = models.CharField(max_length=50, blank=True, default="")
    birthday = models.DateField(blank=True, null=True, default=None)
    gender = models.CharField(max_length=6, blank=True, default="")
    about = models.TextField(blank=True, default="")
