from django.urls import path, reverse, reverse_lazy


from .views import LoginView, LogoutView, RegisterView

app_name = "auth_custom"


urlpatterns = [

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register")
]