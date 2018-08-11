from django import views
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ChatForm
from .models import Message
from .utils import aligned_range_of_pages


class ChatView(views.View):
    template = "chat/chat.html"

    def get(self, request, page=1):
        if request.user.is_authenticated:
            paginator = Paginator(
                Message.objects.all().order_by("-date", "-time"),
                10
            )
            if page not in paginator.page_range:
                raise Http404()
            # TODO: refactor this
            aligned_pages = aligned_range_of_pages(
                page=page,
                range_length=5,
                last_page=paginator.num_pages
            )
            context = {
                "form": ChatForm(),
                "messages": reversed(paginator.get_page(page).object_list),
                "current_page": page,
                "pages": aligned_pages,
                "username": request.user.username
            }
            return render(request, self.template, context=context)
        else:
            return redirect(reverse("auth_custom:login"))

    def post(self, request, page=1):
        form = ChatForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                Message(
                    name=request.user.username,
                    text=form.cleaned_data["message"]
                ).save()
                return redirect("chat:chat", page=page)
            else:
                return redirect(reverse("auth_custom:login"))
        else:
            context = {
                "form": ChatForm()
            }
            return render(request, self.template, context=context)
