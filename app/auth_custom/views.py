from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "auth_custom/login.html"
    redirect_authenticated_user = False

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        status_messages = messages.get_messages(self.request)
        context_data.update({
            'status_messages': status_messages
        })
        return context_data

    def get_success_url(self):
        username = self.request.POST['username']
        return reverse('pages:page', kwargs={'username': username})


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("auth_custom:login")


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "auth_custom/register.html"
    template_name_suffix = ""
    success_url = reverse_lazy('auth_custom:login')

    def get_success_message(self, cleaned_data):
        return f'User {cleaned_data["username"]} was successfully created!'

