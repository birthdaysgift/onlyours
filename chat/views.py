import time

from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Message2All


def chat(request):
    if "username" not in request.session:
        return redirect(reverse("Login page name"))
    messages = Message2All.objects.all()
    if request.method == "POST" and request.POST["message"]:
        context = {"message": request.POST["message"]}
        msg_datetime = time.gmtime(time.time())
        msg_date = time.strftime("%Y-%m-%d", msg_datetime)
        msg_time = time.strftime("%X", msg_datetime)
        name = request.session["username"]
        text = request.POST["message"]
        Message2All(date=msg_date, time=msg_time, name=name, text=text).save()

        return redirect("Chat page name")
    return render(request, "chat/chat.html", context={"messages": messages})


def index(request):
    return redirect("login/")


def login(request):
    if request.method == "POST":
        try:
            User.objects.get(name=request.POST["username"],
                             password=request.POST["password"])
        except ObjectDoesNotExist:
            context = {"error_message": "Wrong username or password."}
            return render(request, "chat/login.html", context=context)
        else:
            request.session["username"] = request.POST["username"]
            return redirect(reverse("Chat page name"))
    return render(request, "chat/login.html")


def logout(request):
    del request.session["username"]
    return redirect(reverse("Login page name"))


def register(request):
    context = dict()
    if request.method == "POST":
        if request.POST["password"] != request.POST["confirm_password"]:
            context["error_message"] = "Passwords are different."
            return render(request, "chat/register.html", context=context)
        try:
            User(name=request.POST["username"],
                 password=request.POST["password"]).save()
        except IntegrityError:
            context["error_message"] = "This username already exists."
            return render(request, "chat/register.html", context=context)
        else:
            context["success_message"] = "{} have been registered!" \
                .format(request.POST["username"])
            return render(request, "chat/register.html", context=context)
    return render(request, "chat/register.html", context=context)
