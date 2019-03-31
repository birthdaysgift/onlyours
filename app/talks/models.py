from django.conf import settings
from django.db import models
from django.db.models import Q

from auth_custom.models import User

from .exceptions import DialogDoesNotExist


class PublicMessage(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name='sent_public_messages'
    )

    def __str__(self):
        return f'#{self.id} [{self.date} {self.time}] {self.sender.username}: '\
               f'{self.text[:30]}'


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


class PrivateMessage(models.Model):
    objects = PrivateMessageQuerySet.as_manager()

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name='received_messages'
    )

    def __str__(self):
        return f'#{self.id} [{self.date} {self.time}] {self.sender.username}: '\
               f'{self.text[:30]}'
