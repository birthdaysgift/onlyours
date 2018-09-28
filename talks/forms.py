from django import forms


class TalksForm(forms.Form):
    message = forms.CharField()