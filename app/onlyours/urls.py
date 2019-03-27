from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from talks.views import RedirectToTalksView


urlpatterns = [
    path("", RedirectToTalksView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path("auth/", include("auth_custom.urls")),
    path("pages/", include("pages.urls")),
    path("talks/", include("talks.urls")),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
