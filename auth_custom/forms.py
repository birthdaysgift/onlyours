from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
