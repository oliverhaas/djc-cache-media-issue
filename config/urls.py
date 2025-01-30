from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import include, path


def index_with_icon(request):
    return render(request, "index.html")


urlpatterns = [
    # User management
    path("", index_with_icon),
    # django-components urls to serve js/css
    path("", include("django_components.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
