from auth_custom.models import User
from Onlyours.settings import AUTH_USER_MODEL

from django.db import models
from django.db.models import Q


class DialogDoesNotExist(Exception):
    pass


class PublicMessage(models.Model):
    objects = models.Manager()

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=0,
                               related_name="sender")
    text = models.TextField()

    def __str__(self):
        return f"#{self.id} [{self.date} {self.time}] {self.sender.name}: " \
               f"{self.text}"


class PrivateMessageQuerySet(models.QuerySet):
    def from_dialog(self, username1, username2):
        try:
            user1 = User.objects.get(username=username1)
            user2 = User.objects.get(username=username2)
        except User.DoesNotExist:
            raise DialogDoesNotExist
        return self.filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
        )


class PrivateMessage(PublicMessage):
    objects = PrivateMessageQuerySet.as_manager()

    receiver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                 related_name="receiver")

    def __str__(self):
        return f"#{self.id} [{self.date} {self.time}] {self.sender} -> " \
               f"{self.receiver}: {self.text}"
