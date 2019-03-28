from django.core.paginator import InvalidPage, Paginator
from django.http import Http404

from .models import Post


def get_posts_for(page_owner, page=1, check_user=None):
    posts = page_owner.received_posts.all()
    posts = posts.select_related('sender')
    posts = posts.order_by("-date", "-time")
    paginator = Paginator(posts, per_page=10)
    try:
        posts_page = paginator.page(page)
    except InvalidPage:
        raise Http404(f'Posts page `{page}` does not exists.')
    posts = posts_page.object_list
    if check_user is not None:
        posts.attach_likes(check_user=check_user)
    if posts_page.has_next():
        next_posts_page = posts_page.next_page_number()
    else:
        next_posts_page = None
    return {'posts': posts, 'next_posts_page': next_posts_page}
