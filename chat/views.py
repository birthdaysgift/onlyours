from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect


def index(request):
    return redirect("login/")


def login(request):
    context = {
        "username": request.POST["username"],
        "password": request.POST["password"]
    } if request.method == "POST" else None
    return render(request, "chat/test.html", context=context)


def register(request):
    if request.method == "POST":
        pass
    return render(request, "chat/register.html", context=dict())
