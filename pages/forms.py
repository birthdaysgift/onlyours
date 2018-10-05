from django import forms

from auth_custom.models import User


class EditPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar", "status", "birthday",
                  "gender", "city", "about"]
        widgets = {
            "gender": forms.Select(choices=(
                ("Male", "Male"),
                ("Female", "Female"),
                ("", "None")
            )),
        }

