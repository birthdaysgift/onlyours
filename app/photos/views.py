from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename

from auth_custom.models import User
from .forms import AddPhotoForm
from .models import PostedPhoto, Photo


def detail_photo(request, username=None, posted_photo_id=None):
    if request.is_ajax():
        template_name = 'photos/ajax/detail_photo.html'
        posted_photo = get_object_or_404(PostedPhoto, id=posted_photo_id)

        posted_photo.n_likes = posted_photo.users_who_liked.count()
        posted_photo.n_dislikes = posted_photo.users_who_disliked.count()

        posted_photo.is_liked = posted_photo.liked_by(request.user)
        posted_photo.is_disliked = posted_photo.disliked_by(request.user)

        context = {'posted_photo': posted_photo}
        return render(request, template_name, context=context)
    raise Http404()


def all_photos(request, username=None):
    if request.is_ajax():
        template_name = "photos/ajax/all_photos.html"
        page_owner = get_object_or_404(User, username=username)
        posted_photos = page_owner.get_posted_photos()
        context = {
            "posted_photos": posted_photos,
            "page_owner": page_owner,
            "photo_form": AddPhotoForm()
        }
        return render(request, template_name, context=context)
    raise Http404()


def add_photo(request, username=None):
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


def delete_photo(request, username=None, posted_photo_id=None):
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
    raise Http404()


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
    raise Http404()
