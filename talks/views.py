from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from auth_custom.models import User
from pages.views import get_friends_of

from .forms import TalksForm
from .models import PublicMessage, PrivateMessage, DialogDoesNotExist
from .utils import aligned_range_of_pages


class TalksView(LoginRequiredMixin, views.View):
    login_url = reverse_lazy("auth_custom:login")

    template = "talks/talks.html"

    def get(self, request, receiver_name="global", page_num=1):
        if receiver_name == "global":
            messages = PublicMessage.objects.all().order_by("-date",
                                                            "-time")
        else:
            try:
                messages = PrivateMessage.objects.from_dialog(
                    request.user.username,
                    receiver_name
                ).order_by("-date", "-time")
            except DialogDoesNotExist:
                raise Http404
        messages_rows = PrivateMessage.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related("sender", "receiver")\
            .distinct("sender").distinct("receiver")
        contacts = []
        for row in messages_rows:
            if row.sender == request.user:
                contacts.append(row.receiver)
            else:
                contacts.append(row.sender)
        paginator = Paginator(messages, 30)
        context = {
            "form": TalksForm(),
            "contacts": contacts,
            "friends": get_friends_of(request.user),
            "messages": reversed(paginator.page(page_num)),
            "pages": aligned_range_of_pages(
                page=page_num,
                last_page=paginator.num_pages
            ),
            "receiver_name": receiver_name,
            "current_user": request.user
        }
        return render(request, self.template, context=context)

    def post(self, request, receiver_name="global", page_num=1):
        form = TalksForm(request.POST)
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
                receiver=get_object_or_404(User, username=receiver_name),
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
