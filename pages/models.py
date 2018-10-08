from django.db import models

from auth_custom.models import User
from Onlyours.settings import AUTH_USER_MODEL


class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               default=0, related_name="post_sender")
    receiver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                 default=0, related_name="post_receiver")
    text = models.TextField()


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="user2")


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="to_user")

    class Meta:
        unique_together = ("from_user", "to_user")