from django.db import models

from auth_custom.models import User


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