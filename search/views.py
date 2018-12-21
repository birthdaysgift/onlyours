from django.shortcuts import render
from django.views import View


class SearchPageView(View):
    template_name = 'search/users.html'

    def get(self, request):
        return render(request, self.template_name)
