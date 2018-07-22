from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control"
            }
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        label="Password:",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        label="Password:",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password_confirm = forms.CharField(
        label="Confirm password:",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
