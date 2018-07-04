from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50, unique=True)
    password = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    date = models.DateField()
    time = models.TimeField()
    user_id = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return "{} {} {}".format(self.user_id, self.time, self.date)
