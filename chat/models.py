from django.db import models


class Message(models.Model):

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    name = models.TextField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return f"#{self.id} [{self.date} {self.time}] {self.name}: {self.text}"
