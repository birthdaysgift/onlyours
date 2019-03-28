from django.conf import settings
from django.db import models


class PostQuerySet(models.QuerySet):
    def attach_likes(self, check_user=None):
        for post in self:
            likes = PostLike.objects.filter(post=post)
            dislikes = PostDislike.objects.filter(post=post)
            setattr(post, 'likes', likes)
            setattr(post, 'dislikes', dislikes)
            if check_user:
                setattr(post, 'is_liked', post.liked_by(check_user))
                setattr(post, 'is_disliked', post.disliked_by(check_user))
        return self


class Post(models.Model):
    objects = PostQuerySet.as_manager()

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name="sent_posts"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name="received_posts"
    )
    text = models.TextField()

    def liked_by(self, user):
        is_liked = PostLike.objects.filter(
            post=self, user=user
        ).exists()
        return is_liked

    def disliked_by(self, user):
        is_disliked = PostDislike.objects.filter(
            post=self, user=user
        ).exists()
        return is_disliked

    def __str__(self):
        return f'{self.sender} -> {self.receiver} :: {self.text[:30]}'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='like_user_new'
    )

    def __str__(self):
        return f'{self.user} :: [{self.post}]'


class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE,
        related_name='dislike_user_new'
    )

    def __str__(self):
        return f'{self.user} :: [{self.post}]'
