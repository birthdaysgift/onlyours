from django import views
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


class IndexView(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("chat:chat", kwargs={"page": 1}))
        else:
            return redirect(reverse("auth_custom:login"))


class LoginView(views.View):
    template = "auth_custom/login.html"

    def get(self, request):
        context = {
            "form": LoginForm()
        }
        return render(request, self.template, context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        # TODO: how to change default browsers(!) validation
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect(reverse("chat:chat", kwargs={"page": 1}))
            else:
                context = {
                    "error_message": "Wrong username or password.",
                    "form": LoginForm()
                }
                return render(request, self.template, context=context)
        else:
            context = {
                "form": LoginForm()
            }
            return render(request, self.template, context=context)


class RegisterView(views.View):
    template = "auth_custom/register.html"

    def get(self, request):
        context = {
            "form": RegisterForm()
        }
        return render(request, self.template, context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                ).save()
            except IntegrityError as e:
                context = {
                    "error_message": "This username already exists.",
                    "form": RegisterForm(),
                }
                return render(request, "chat/register.html", context=context)
            context = {
                "form": RegisterForm(),
                "success_message": "{} have been registered!".format(
                    form.cleaned_data["username"]
                )
            }
            return render(request, self.template, context=context)
        else:
            return render(request, self.template, context={"form": form})