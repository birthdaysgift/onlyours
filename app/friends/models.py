import random

from django.conf import settings
from django.db import models
from django.db.models import Q

from auth_custom.models import User


class ArgumentsError(Exception):
    pass


class FriendshipManager(models.Manager):

    def get_friends_of(self, user, strict_to=None, order_by_attr=None,
                       random_order=False):
        if order_by_attr and random_order:
            raise ArgumentsError(
                'You can\'t set both `order_by_attr` and '
                '`random_order` arguments.'
            )

        user_friend_pairs = self.filter(Q(user1=user) | Q(user2=user))
        user_friend_pairs = user_friend_pairs.select_related("user1", "user2")

        friends = []
        for pair in user_friend_pairs:
            if pair.user1 == user:
                friends.append(pair.user2)
            else:
                friends.append(pair.user1)

        if order_by_attr:
            friends.sort(
                key=lambda friend: getattr(friend, order_by_attr),
                reverse=order_by_attr.startswith('-')
            )
        if random_order:
            random.shuffle(friends)
        if strict_to:
            friends = friends[:strict_to]
        return friends

    def is_friends(self, user1, user2):
        result = self.filter(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).exists()
        return result


class FriendshipRequestManager(models.Manager):
    def who_sent_request(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).exists():
            return user1
        if self.filter(from_user=user2, to_user=user1).exists():
            return user2
        return None


class Friendship(models.Model):
    objects = FriendshipManager()

    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="user1"
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="user2"
    )

    def __str__(self):
        return f'{self.user1} <-> {self.user2}'


class FriendshipRequest(models.Model):
    objects = FriendshipRequestManager()

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_user"
    )

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'

    class Meta:
        unique_together = ("from_user", "to_user")
