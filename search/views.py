from django.shortcuts import render
from django.views import View

from . import forms


class SearchPageView(View):
    template_name = 'search/users.html'

    def get(self, request):
        context = {
            'form': forms.UserSearchForm()
        }
        return render(request, self.template_name, context=context)
