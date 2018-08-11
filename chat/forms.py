from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Write a message..."
            }
        )
    )
