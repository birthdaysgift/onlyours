from django.db import models


class User(models.Model):
    name = models.TextField(max_length=50, primary_key=True)
    password = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Message2All(models.Model):
    date = models.DateField()
    time = models.TimeField()
    name = models.TextField(max_length=50)
    # blank=false doesnt work, dont know why
    text = models.TextField(blank=False)

    def __str__(self):
        return "{} {} {}".format(self.name, self.date, self.time)
