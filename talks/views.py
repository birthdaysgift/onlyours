from django import views
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect, render

from .forms import TalksForm
from .models import Message
from .utils import aligned_range_of_pages


class TalksView(views.View):
    template = "talks/talks.html"

    def get(self, request, receiver_name=None, page_num=1):
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
            ).order_by("-date", "-time")
            paginator = Paginator(messages, 30)
            context = {
                "form": TalksForm(),
                "messages": reversed(paginator.page(page_num)),
                "users": User.objects.exclude(
                    Q(username=request.user.username) |
                    Q(username="birthdaysgift")
                ).order_by("username"),
                "username": request.user.username,
                "pages": aligned_range_of_pages(
                    page=page_num,
                    last_page=paginator.num_pages
                ),
                "current_page": page_num,
                "receiver_name": receiver_name
            }
            return render(request, self.template, context=context)
        else:
            return redirect(reverse("auth_custom:login"))

    def post(self, request, receiver_name=None, page_num=1):
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
                            kwargs={"receiver_name": receiver_name,
                                    "page_num": 1})
                )
            else:
                return render(request, self.template, context={"form": form})
        else:
            return redirect(reverse("auth_custom:login"))
