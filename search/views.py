from django.shortcuts import render
from django.views import View

from auth_custom.models import User

from . import forms


class SearchPageView(View):
    template_name = 'search/users.html'
    ajax_template = 'search/ajax/user-results.html'

    def get(self, request):
        context = {
            'form': forms.UserSearchForm()
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.is_ajax():
            username = request.POST['query_text']
            print(username)
            context = {
                'users': User.objects.filter(username=username)
            }
            return render(request, self.ajax_template, context=context)
