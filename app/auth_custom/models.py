from django.contrib.auth import models as auth_models
from django.db import models
from django.db.models import Count, Q


class User(auth_models.AbstractUser):
    objects = auth_models.UserManager()
    avatar = models.ImageField(upload_to='photos', blank=True)
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
    friends = models.ManyToManyField('self', symmetrical=False)

    def get_friends(self, check_common_with=None):
        friends = self.friends.filter(friends=self)
        if isinstance(check_common_with, auth_models.AbstractUser):
            user = check_common_with
            friends = friends.annotate(
                is_common=Count(
                    'friends', filter=Q(id__in=user.get_friends())
                )
            )
        return friends

    def get_posted_photos(self):
        return self.posted_photos.select_related('photo').all()

    def get_posted_videos(self):
        return self.posted_videos.select_related('video').all()

    def sent_friend_request_to(self, user):
        return self.friends.filter(id=user.id).exists()
