from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView

from auth_custom.models import User

from .forms import EditPageForm


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")

    template = "pages/page.html"

    def get(self, request, username=None):
        if username is not None:
            user = get_object_or_404(User, username=username)
            context = {
                "user": user,
                "current_user": request.user
            }
            return render(request, self.template, context=context)


class EditView(UpdateView):
    template_name = "pages/edit.html"
    template_name_suffix = ""
    success_url = reverse_lazy("talks:talk", kwargs={"receiver_name": "global",
                                                     "page_num": 1})
    form_class = EditPageForm
    model = User