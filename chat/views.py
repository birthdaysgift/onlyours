from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .models import User


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
            context = {"username": request.POST["username"],
                       "password": request.POST["password"]}
            return render(request, "chat/test.html", context=context)
    return render(request, "chat/login.html", context=dict())


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
            context["success_message"] = "{} have been registered!"\
                .format(request.POST["username"])
            return render("chat/register.html", context=context)
    return render(request, "chat/register.html", context=context)
