from django.shortcuts import render
from django.views import View

from auth_custom.models import User

class PageView(View):
    template = "pages/page.html"

    def get(self, request, username=None):
        if username is not None:
            user = User.objects.get(username=username)
            context = {
                "user": user
            }
            return render(request, self.template, context=context)
