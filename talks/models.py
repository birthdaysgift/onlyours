from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    objects = models.Manager()

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 related_name="receiver")
    text = models.TextField()

    def __str__(self):
        return f"#{self.id} [{self.date} {self.time}] {self.sender} -> " \
               f"{self.receiver}: {self.text}"
