from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.db.models import Count, Q
from django.http import Http404


def get_posts_for(user, page=1, count_likes=False, attach_senders=True,
                  attach_users_who_liked=False, check_user=None):
    """
    Returns QuerySet which contains posts received by `user`.
    Params:
        page - number of page
        count_likes - adds `n_likes` and `n_dislikes` fields to each post
        attach_sender - adds `sender` field to each post
        attach_users_who_liked - adds `users_who_liked` and `users_who_disliked`
                                 fields to each post
        check_user - accepts User object and adds `is_liked` and `is_disliked`
                     fields to each post, they represent if this post was liked
                     or disliked by user `check_user`
    """
    posts = user.received_posts.order_by('-date', '-time')
    try:
        posts_page = Paginator(posts, per_page=10).page(page)
    except InvalidPage:
        raise Http404(f'Posts page `{page}` does not exists.')
    posts = posts_page.object_list

    if attach_senders:
        posts = posts.select_related('sender')
    if attach_users_who_liked:
        posts = posts.prefetch_related(
            'users_who_liked', 'users_who_disliked'
        )
    if count_likes:
        posts = posts.annotate(
            n_likes=Count('users_who_liked'),
            n_dislikes=Count('users_who_disliked')
        )
    if isinstance(check_user, get_user_model()):
        posts = posts.annotate(
            is_liked=Count(
                'users_who_liked',
                filter=Q(users_who_liked=check_user)
            ),
            is_disliked=Count(
                'users_who_disliked',
                filter=Q(users_who_disliked=check_user)
            )
        )
    # Monkey patching fields on QuerySet have to be done
    # after all calls modifications of QuerySet, otherwise
    # monkey patched field will disappear
    posts.next_page_num = (page+1) if posts_page.has_next() else None
    return posts


class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name="sent_posts"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name="received_posts"
    )
    users_who_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_posts'
    )
    users_who_disliked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='disliked_posts'
    )

    def liked_by(self, user):
        is_liked = self.users_who_liked.filter(id=user.id)
        return is_liked

    def disliked_by(self, user):
        is_disliked = self.users_who_disliked.filter(id=user.id)
        return is_disliked

    def __str__(self):
        return f'{self.sender} -> {self.receiver} :: {self.text[:30]}'
