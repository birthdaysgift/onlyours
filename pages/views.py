import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.text import get_valid_filename
from django.views import View


from auth_custom.models import User
from .forms import EditPageForm, AddPostForm, AddPhotoForm, AddVideoForm
from .models import Friendship, FriendshipRequest, Post, UserPhoto, Photo, \
    UserVideo, Video, PostLike, PostDislike


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")
    template_name = "pages/base.html"

    def get(self, request, username=None):
        # get page owner
        page_owner = get_object_or_404(User, username=username)

        # get posts and likes/dislikes for them
        posts = Post.objects.filter(receiver=page_owner)
        posts = posts.select_related('sender')
        posts = posts.order_by("-date", "-time")
        for post in posts:
            likes = PostLike.objects.filter(post=post)
            likes = likes.select_related('user')
            dislikes = PostDislike.objects.filter(post=post)
            dislikes = dislikes.select_related('user')
            setattr(post, 'likes', likes)
            setattr(post, 'dislikes', dislikes)
            is_liked = PostLike.objects.filter(
                post=post, user=request.user
            ).exists()
            is_disliked = PostDislike.objects.filter(
                post=post, user=request.user
            ).exists()
            setattr(post, 'is_liked', is_liked)
            setattr(post, 'is_disliked', is_disliked)

        # get user_photos
        user_photos = UserPhoto.objects.filter(user=page_owner)
        user_photos = user_photos.select_related("user", "photo")[:6]

        # get user_videos
        user_videos = UserVideo.objects.filter(user=page_owner)
        user_videos = user_videos.select_related("user", "video")[:6]

        # get friends
        friends = Friendship.objects.get_friends_of(page_owner)
        max_friends = 6  # max friends on friends-panel in page.html
        if len(friends) < max_friends:
            friends = random.sample(friends, len(friends))
        else:
            friends = random.sample(friends, max_friends)

        # get friendship status
        # friend:     user <-> page_owner
        # requested:  user --> page_owner
        # requesting: user <-- page_owner
        friendship_status = None
        if request.user in friends:
            friendship_status = "friend"
        requested = FriendshipRequest.objects.filter(
            from_user=request.user, to_user=page_owner
        ).exists()
        if requested:
            friendship_status = "requested"
        requesting = FriendshipRequest.objects.filter(
            from_user=page_owner, to_user=request.user
        ).exists()
        if requesting:
            friendship_status = "requesting"

        context = {
            "form": AddPostForm(),
            "page_owner": page_owner,
            "posts": posts,
            "friends": friends,
            "user_photos": user_photos,
            "friendship_status": friendship_status,
            "user_videos": user_videos
        }
        return render(request, self.template_name, context=context)

    def post(self, request, username=None):
        form = AddPostForm(request.POST)
        if form.is_valid():
            receiver = get_object_or_404(User, username=username)
            Post(
                sender=request.user,
                receiver=receiver,
                text=form.cleaned_data["text"]
            ).save()
            url = reverse('pages:page', kwargs={'username': username})
            return redirect(url)
        else:
            return render(request, self.template_name, context={"form": form})


class DeletePostView(View):
    template_name = 'pages/ajax/delete_post.html'

    def get(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.is_ajax() and request.user == page_owner:
            post = Post.objects.get(id=post_id)
            return render(request, self.template_name, context={"post": post})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)

    def post(self, request, username=None, post_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            Post.objects.get(id=post_id).delete()
        url = reverse('pages:page', kwargs={"username": username})
        return redirect(url)


class LikePostView(View):
    def get(self, request, username=None, post_id=None):
        if request.is_ajax():
            post = Post.objects.get(id=post_id)
            like = PostLike.objects.filter(user=request.user, post=post)
            dislike = PostDislike.objects.filter(user=request.user, post=post)
            if like.exists():
                like[0].delete()
            else:
                if dislike.exists():
                    dislike[0].delete()
                PostLike(user=request.user, post=post).save()
            return HttpResponse()


class DislikePostView(View):
    def get(self, request, username=None, post_id=None):
        if request.is_ajax():
            post = Post.objects.get(id=post_id)
            like = PostLike.objects.filter(user=request.user, post=post)
            dislike = PostDislike.objects.filter(user=request.user, post=post)
            if dislike.exists():
                dislike[0].delete()
            else:
                if like.exists():
                    like[0].delete()
                PostDislike(user=request.user, post=post).save()
            return HttpResponse()


class EditView(LoginRequiredMixin, View):
    template_name = "pages/edit.html"

    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            form = EditPageForm(instance=request.user)
            return render(request, self.template_name, context={"form": form})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)

    def post(self, request, username=None):
        form = EditPageForm(request.POST, request.FILES, instance=request.user)
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            if form.is_valid():
                form.save()
                kwargs = {"username": request.user.username}
                url = reverse('pages:page', kwargs=kwargs)
                return redirect(url)
            return render(request, self.template_name, context={"form": form})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class SendFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest(
                    from_user=request.user, to_user=page_owner
                ).save()
            # it is raised when such FriendshipRequest already exists
            except IntegrityError:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class CancelFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest.objects.get(
                    from_user=request.user, to_user=page_owner
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AcceptFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            friendship_request = FriendshipRequest.objects.filter(
                from_user=page_owner, to_user=request.user
            )
            if friendship_request.exists():
                friendship_request.delete()
                Friendship(user1=request.user, user2=page_owner).save()
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class DenyFriendRequestView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user != page_owner:
            try:
                FriendshipRequest.objects.get(
                    from_user=page_owner, to_user=request.user
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class RemoveFriendView(View):
    def get(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                Friendship.objects.get(
                    Q(user1=page_owner, user2=request.user) |
                    Q(user1=request.user, user2=page_owner)
                ).delete()
            except FriendshipRequest.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)


class FriendsListView(View):
    template_name = "pages/ajax/all_friends.html"

    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = User.objects.get(username=username)
            friends = Friendship.objects.get_friends_of(page_owner)
            session_user_friends = Friendship.objects.get_friends_of(request.user)
            friends.sort(key=lambda e: e.username.lower())
            context = {
                "friends": friends,
                "session_user_friends": session_user_friends
            }
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class DetailPhotoView(View):
    template_name = 'pages/ajax/detail_photo.html'

    def get(self, request, username=None, userphoto_id=None):
        if request.is_ajax():
            userphoto = get_object_or_404(UserPhoto, id=userphoto_id)
            context = {'userphoto': userphoto}
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class PhotosListView(View):
    template_name = "pages/ajax/all_photos.html"

    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = get_object_or_404(User, username=username)
            user_photos = UserPhoto.objects.filter(user=page_owner)
            user_photos = user_photos.select_related('photo')
            context = {
                "user_photos": user_photos,
                "page_owner": page_owner,
                "photo_form": AddPhotoForm()
            }
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AddNewPhotoView(View):
    template_name = 'pages/ajax/all_photos.html'

    def post(self, request, username=None):
        form = AddPhotoForm(request.POST, request.FILES)
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner and form.is_valid():
            form.save()

            filename = get_valid_filename(form.cleaned_data['file'].name)
            photo = get_object_or_404(Photo, file=filename)

            user = get_object_or_404(User, username=username)
            UserPhoto(user=user, photo=photo).save()
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class DeletePhotoView(View):
    def get(self, request, username=None, userphoto_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                UserPhoto.objects.get(id=userphoto_id).delete()
            except UserPhoto.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)


class DetailVideoView(View):
    template_name = 'pages/ajax/detail_video.html'

    def get(self, request, username=None, video_id=None):
        if request.is_ajax():
            video = get_object_or_404(Video, id=video_id)
            return render(request, self.template_name, context={'video': video})
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class VideosListView(View):
    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = get_object_or_404(User, username=username)
            user_videos = UserVideo.objects.filter(user=page_owner)
            user_videos = user_videos.select_related("video")
            context = {
                "user_videos": user_videos,
                "page_owner": page_owner,
                "video_form": AddVideoForm()
            }
            return render(request, "pages/ajax/all_videos.html", context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AddNewVideoView(View):
    template_name = "pages/ajax/add_video.html"

    def post(self, request, username=None):
        page_owner = get_object_or_404(User, username=username)
        form = AddVideoForm(request.POST, request.FILES)
        if request.user == page_owner and form.is_valid():
            form.save()

            filename = get_valid_filename(form.cleaned_data['file'].name)
            video = get_object_or_404(Video, file=filename)
            user = get_object_or_404(User, username=username)
            UserVideo(user=user, video=video).save()

            kwargs = {'username': username}
        url = reverse('pages:page', kwargs=kwargs)
        return redirect(url)


class DeleteVideoView(View):
    def get(self, request, username=None, uservideo=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                UserVideo.objects.get(id=uservideo).delete()
            except UserVideo.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)
