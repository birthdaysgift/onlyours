from django.urls import path

from search import views

app_name = 'search'

urlpatterns = [
    path('users/', views.SearchPageView.as_view(), name='users'),
]