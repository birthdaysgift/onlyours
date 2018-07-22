import time

from django import views
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ChatForm, LoginForm, RegisterForm
from .models import User, Message2All


class ChatView(views.View):

    def get(self, request):
        if "username" not in request.session:
            return redirect(reverse("Login page name"))
        context = {
            "form": ChatForm(),
            "messages": Message2All.objects.all()
        }
        return render(request, "chat/chat.html", context=context)

    def post(self, request):
        form = ChatForm(request.POST)
        if form.is_valid():
            msg_datetime = time.gmtime(time.time())
            msg_date = time.strftime("%Y-%m-%d", msg_datetime)
            msg_time = time.strftime("%X", msg_datetime)
            name = request.session["username"]
            text = form.cleaned_data["message"]
            Message2All(date=msg_date, time=msg_time, name=name,
                        text=text).save()
            return redirect("Chat page name")


def index(request):
    return redirect("login/")


class LoginView(views.View):

    def get(self, request):
        context = {
            "form": LoginForm()
        }
        return render(request, "chat/login.html", context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(name=form.cleaned_data["username"],
                                 password=form.cleaned_data["password"])
            except ObjectDoesNotExist:
                context = {
                    "error_message": "Wrong username or password.",
                    "form": LoginForm()
                }
                return render(request, "chat/login.html", context=context)
            else:
                request.session["username"] = form.cleaned_data["username"]
                return redirect(reverse("Chat page name"))


def logout(request):
    del request.session["username"]
    return redirect(reverse("Login page name"))


class RegisterView(views.View):

    def get(self, request):
        context = {
            "form": RegisterForm()
        }
        return render(request, "chat/register.html", context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != \
                    form.cleaned_data["password_confirm"]:
                context = {
                    "error_message": "Passwords are different.",
                    "form": RegisterForm()
                }
                return render(request, "chat/register.html", context=context)
            try:
                User(name=form.cleaned_data["username"],
                     password=form.cleaned_data["password"]).save()
            except IntegrityError:
                context = {
                    "error_message": "This username already exists.",
                    "form": RegisterForm()
                }
                return render(request, "chat/register.html", context=context)
            else:
                context = {
                    "form": RegisterForm(),
                    "success_message": "{} have been registered!".format(
                        form.cleaned_data["username"]
                    )
                }
                return render(request, "chat/register.html", context=context)
