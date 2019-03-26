from django import forms


class AddPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
