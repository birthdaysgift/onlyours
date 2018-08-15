from django import views
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import TalksForm
from .models import PublicMessage, PrivateMessage
from .utils import aligned_range_of_pages


class TalksView(views.View):
    template = "talks/talks.html"

    def get(self, request, receiver_name="global", page_num=1):
        if request.user.is_authenticated:
            if receiver_name == "global":
                messages = PublicMessage.objects.all().order_by("-date",
                                                                "-time")
                paginator = Paginator(messages, 30)
                context = {
                    "form": TalksForm(),
                    "contacts": User.objects.exclude(
                        Q(username=request.user.username) |
                        Q(username="birthdaysgift")
                    ).order_by("username"),
                    "messages": reversed(paginator.page(page_num)),
                    "current_user": request.user
                }
                return render(request, self.template, context=context)
            messages = PrivateMessage.objects.from_dialog(
                request.user.username,
                receiver_name
            ).order_by("-date", "-time")
            paginator = Paginator(messages, 30)
            context = {
                "form": TalksForm(),
                "messages": reversed(paginator.page(page_num)),
                "contacts": User.objects.exclude(
                    Q(username=request.user.username) |
                    Q(username="birthdaysgift")
                ).order_by("username"),
                "current_user": request.user,
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
                if receiver_name == "global":
                    PublicMessage(
                        sender=request.user,
                        text=form.cleaned_data["message"]
                    ).save()
                    return redirect(
                        reverse("talks:talk", kwargs={
                            "receiver_name": receiver_name,
                            "page_num": 1
                        })
                    )
                PrivateMessage(
                    sender=request.user,
                    receiver=User.objects.get(username=receiver_name),
                    text=form.cleaned_data["message"]
                ).save()
                return redirect(
                    reverse("talks:talk", kwargs={
                        "receiver_name": receiver_name,
                        "page_num": 1
                    })
                )
            else:
                return render(request, self.template, context={"form": form})
        else:
            return redirect(reverse("auth_custom:login"))
