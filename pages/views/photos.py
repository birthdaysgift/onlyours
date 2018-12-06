from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views import View


from auth_custom.models import User
from ..forms import AddPhotoForm
from ..models import UserPhoto, Photo


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


class AddPhotoView(View):
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
