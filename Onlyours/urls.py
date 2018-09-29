from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy

from Onlyours import settings

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("talks:talk", kwargs={
        "receiver_name": "global",
        "page_num": 1
    })), name="index"),
    path('admin/', admin.site.urls),
    path("auth/", include("auth_custom.urls")),
    path("pages/", include("pages.urls")),
    path("talks/", include("talks.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
