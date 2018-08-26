from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View

from auth_custom.models import User


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")

    template = "pages/page.html"

    def get(self, request, username=None):
        if username is not None:
            user = get_object_or_404(User, username=username)
            context = {
                "user": user
            }
            return render(request, self.template, context=context)


class ChangeView(View):
    pass
