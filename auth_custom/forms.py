from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    # TODO: change default password validation (at least 8 symbols including
    # TODO: letters and numbers)
    class Meta(UserCreationForm.Meta):
        model = User
