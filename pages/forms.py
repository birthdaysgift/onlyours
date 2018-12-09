from django import forms

from auth_custom.models import User


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


