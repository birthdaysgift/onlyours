from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views import View

from auth_custom.models import User
from .forms import AddPhotoForm
from .models import PostedPhoto, Photo


class DetailPhotoView(View):
    template_name = 'photos/ajax/detail_photo.html'

    def get(self, request, username=None, posted_photo_id=None):
        if request.is_ajax():
            posted_photo = get_object_or_404(PostedPhoto, id=posted_photo_id)
            likes = posted_photo.users_who_liked.all()
            dislikes = posted_photo.users_who_disliked.all()
            setattr(posted_photo, 'likes', likes)
            setattr(posted_photo, 'dislikes', dislikes)
            is_liked = posted_photo.liked_by(request.user)
            is_disliked = posted_photo.disliked_by(request.user)
            setattr(posted_photo, 'is_liked', is_liked)
            setattr(posted_photo, 'is_disliked', is_disliked)
            context = {'posted_photo': posted_photo}
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class PhotosListView(View):
    template_name = "photos/ajax/all_photos.html"

    def get(self, request, username=None):
        if request.is_ajax():
            page_owner = get_object_or_404(User, username=username)
            posted_photos = page_owner.posted_photos.all()
            posted_photos = posted_photos.select_related('photo')
            context = {
                "posted_photos": posted_photos,
                "page_owner": page_owner,
                "photo_form": AddPhotoForm()
            }
            return render(request, self.template_name, context=context)
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class AddPhotoView(View):
    template_name = 'photos/ajax/all_photos.html'

    def post(self, request, username=None):
        form = AddPhotoForm(request.POST, request.FILES)
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner and form.is_valid():
            form.save()

            filename = get_valid_filename(form.cleaned_data['file'].name)
            photo = get_object_or_404(Photo, file=filename)

            user = get_object_or_404(User, username=username)
            PostedPhoto(user=user, photo=photo).save()
        url = reverse('pages:page', kwargs={'username': username})
        return redirect(url)


class DeletePhotoView(View):
    def get(self, request, username=None, posted_photo_id=None):
        page_owner = get_object_or_404(User, username=username)
        if request.user == page_owner:
            try:
                PostedPhoto.objects.get(id=posted_photo_id).delete()
            except PostedPhoto.DoesNotExist:
                pass
        url = reverse("pages:page", kwargs={"username": username})
        return redirect(url)


def like_photo(request, username=None, posted_photo_id=None):
    if request.is_ajax():
        posted_photo = PostedPhoto.objects.get(id=posted_photo_id)
        if posted_photo.liked_by(request.user):
            posted_photo.users_who_liked.remove(request.user)
        else:
            if posted_photo.disliked_by(request.user):
                posted_photo.users_who_disliked.remove(request.user)
            posted_photo.users_who_liked.add(request.user)
        return HttpResponse()


def dislike_photo(request, username=None, posted_photo_id=None):
    if request.is_ajax():
        posted_photo = PostedPhoto.objects.get(id=posted_photo_id)
        if posted_photo.disliked_by(request.user):
            posted_photo.users_who_disliked.remove(request.user)
        else:
            if posted_photo.liked_by(request.user):
                posted_photo.users_who_liked.remove(request.user)
            posted_photo.users_who_disliked.add(request.user)
        return HttpResponse()
