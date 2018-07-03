from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    password = models.TextField(max_length=100)


class Message(models.Model):
    date = models.DateField()
    time = models.TimeField()
    user_id = models.PositiveIntegerField()
    text = models.TextField()
