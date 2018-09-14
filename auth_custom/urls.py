from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.urls import path, reverse, reverse_lazy


from .views import RegisterView

app_name = "auth_custom"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


urlpatterns = [

    path("login/", LoginView.as_view(
        template_name="auth_custom/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    path("logout/",
         LogoutView.as_view(next_page=reverse_lazy("auth_custom:login")),
         name="logout"),
    path("register/", FormView.as_view(
        template_name="auth_custom/register.html",
        form_class=CustomUserCreationForm,
        success_url=reverse_lazy("talks:talk",
                                 kwargs={"receiver_name": "global",
                                         "page_num": 1})
    ), name="register")
]