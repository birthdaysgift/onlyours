from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect, render

from .forms import TalksForm
from .models import Message


class TalksView(views.View):
    template = "talks/talks.html"

    def get(self, request, receiver_name=None):
        if request.user.is_authenticated:
            if not receiver_name:
                context = {
                    "form": TalksForm(),
                    "users": User.objects.exclude(
                        Q(username=request.user.username) |
                        Q(username="birthdaysgift")
                    ),
                    "username": request.user.username
                }
                return render(request, self.template, context=context)
            user1 = User.objects.get(username=request.user.username)
            user2 = User.objects.get(username=receiver_name)
            messages = Message.objects.filter(
                Q(sender=user1, receiver=user2) |
                Q(sender=user2, receiver=user1)
            )
            context = {
                "form": TalksForm(),
                "messages": messages,
                "users": User.objects.exclude(
                    Q(username=request.user.username) |
                    Q(username="birthdaysgift")
                ),
                "username": request.user.username
            }
            return render(request, self.template, context=context)
        else:
            return redirect(reverse("auth_custom:login"))

    def post(self, request, receiver_name=None):
        form = TalksForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                Message(
                    sender=request.user,
                    receiver=User.objects.get(username=receiver_name),
                    text=form.cleaned_data["message"]
                ).save()
                return redirect(
                    reverse("talks:talks",
                            kwargs={"receiver_name": receiver_name})
                )
            else:
                return render(request, self.template, context={"form": form})
        else:
            return redirect(reverse("auth_custom:login"))
