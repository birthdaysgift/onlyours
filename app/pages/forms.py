from django import forms
from django.utils.translation import gettext_lazy as _

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
        },
        error_messages = {
            'birthday': {
                'invalid': _('Birthday must be in YYYY-MM-DD format.')
            }
        }


