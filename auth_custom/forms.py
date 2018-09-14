from django import forms
from django.forms import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        max_length=50,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="Password:",
        max_length=100,
        widget=forms.PasswordInput()
    )


class RegisterForm(LoginForm):
    password_confirm = forms.CharField(
        label="Confirm password:",
        max_length=100,
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != \
                cleaned_data["password_confirm"]:
            raise ValidationError("Passwords are different.")
        return cleaned_data
