import time

from django import views
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ChatForm, LoginForm, RegisterForm
from .models import User, Message


class ChatView(views.View):

    def get(self, request, page=1):
        if "username" not in request.session:
            return redirect(reverse("login-page-url"))
        last_page = Message.objects.page_nums[-1]
        if not (1 <= page <= last_page):
            raise Http404()
        context = {
            "form": ChatForm(),
            "messages": Message.objects.from_page(page),
            "pages": Message.objects.page_nums,
            "username": request.session["username"]
        }
        return render(request, "chat/chat.html", context=context)

    def post(self, request, page=1):
        form = ChatForm(request.POST)
        if form.is_valid():
            Message(
                name=request.session["username"],
                text=form.cleaned_data["message"]
            ).save()
            return redirect("chat-page-url", page=page)


def index(request):
    return redirect(reverse("login-page-url"))


class LoginView(views.View):

    def get(self, request):
        context = {
            "form": LoginForm()
        }
        return render(request, "chat/login.html", context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        # TODO: what and why is going on when form is invalid?
        if form.is_valid():
            if User.objects.has_unique(
                        name=form.cleaned_data["username"],
                        password=form.cleaned_data["password"]
                    ):
                request.session["username"] = form.cleaned_data["username"]
                return redirect(reverse("chat-page-url", kwargs={"page": 1}))
            else:
                context = {
                    "error_message": "Wrong username or password.",
                    "form": LoginForm()
                }
                return render(request, "chat/login.html", context=context)


def logout(request):
    del request.session["username"]
    return redirect(reverse("login-page-url"))


class RegisterView(views.View):

    def get(self, request):
        context = {
            "form": RegisterForm()
        }
        return render(request, "chat/register.html", context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User(
                    name=form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                ).save()
            except IntegrityError:
                context = {
                    "error_message": "This username already exists.",
                    "form": RegisterForm()
                }
                return render(request, "chat/register.html", context=context)
            context = {
                "form": RegisterForm(),
                "success_message": "{} have been registered!".format(
                    form.cleaned_data["username"]
                )
            }
            return render(request, "chat/register.html", context=context)
        else:
            return render(request, "chat/register.html", context={"form": form})


