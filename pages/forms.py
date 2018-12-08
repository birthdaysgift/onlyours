from django import forms

from auth_custom.models import User
from .models import Photo, Video


class EditPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'status', "first_name", "last_name", "birthday",
                  "gender", "city", "about"]
        widgets = {
            "gender": forms.RadioSelect(choices=(
                ("Male", "Male"),
                ("Female", "Female"),
                ("", "None")
            )),
        }


class AddPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("file", )


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("file", )