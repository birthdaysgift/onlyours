from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "auth_custom/login.html"
    redirect_authenticated_user = False


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("auth_custom:login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "auth_custom/register.html"
    template_name_suffix = ""
    success_url = reverse_lazy("talks:talk", kwargs={"receiver_name": "global",
                                                     "page_num": 1})
