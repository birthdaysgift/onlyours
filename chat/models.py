import math

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models


MESSAGES_ON_PAGE = 10


class MessageQuerySet(models.QuerySet):

    def from_page(self, page_num):
        on_page = slice((page_num-1) * MESSAGES_ON_PAGE,
                        page_num * MESSAGES_ON_PAGE)
        # TODO: simplify this
        return reversed(self.all().order_by("-date", "-time")[on_page])


class MessageManager(models.Manager):

    @property
    def page_nums(self):
        # noinspection PyTypeChecker
        return list(range(1, math.ceil(self.all().count() /
                                       MESSAGES_ON_PAGE) + 1))


class Message(models.Model):

    objects = MessageManager.from_queryset(MessageQuerySet)()

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    name = models.TextField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return "#{id} [{date} {time}] {name}: {text}".format(
            id=self.id,
            date=self.date,
            time=self.time,
            name=self.name,
            text=self.text[:30]
        )


class UserQuerySet(models.QuerySet):

    def has_unique(self, *args, **kwargs):
        try:
            self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False
        return True


class User(models.Model):

    objects = UserQuerySet.as_manager()

    name = models.TextField(max_length=50, primary_key=True)
    password = models.TextField(max_length=100)

    def __str__(self):
        return self.name
