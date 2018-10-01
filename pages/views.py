from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from auth_custom.models import User

from .forms import EditPageForm


class PageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_custom:login")

    template_name = "pages/page.html"

    def get(self, request, username=None):
        if username is not None:
            user = get_object_or_404(User, username=username)
            context = {
                "user": user,
                "current_user": request.user
            }
            return render(request, self.template_name, context=context)


class EditView(LoginRequiredMixin, View):
    template_name = "pages/edit.html"

    def get(self, request, username=None):
        if username != request.user.username:
            return redirect(reverse_lazy(
                "pages:edit",
                kwargs={"username": request.user.username}
            ))
        return render(request, self.template_name, context={
            "form": EditPageForm(instance=request.user)
        })

    def post(self, request, username=None):
        form = EditPageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("pages:page", kwargs={
                "username": request.user.username
            }))
        return render(request, self.template_name, context={"form": form})
