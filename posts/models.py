from django.db import models

from Onlyours.settings import AUTH_USER_MODEL


class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               default=0, related_name="post_sender_new")
    receiver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                 default=0, related_name="post_receiver_new")
    text = models.TextField()

    def __str__(self):
        return f'{self.sender} -> {self.receiver} :: {self.text[:30]}'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='like_user_new')

    def __str__(self):
        return f'{self.user} :: [{self.post}]'


class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='dislike_user_new')

    def __str__(self):
        return f'{self.user} :: [{self.post}]'
