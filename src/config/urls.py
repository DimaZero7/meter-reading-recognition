from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("services.api.urls")),
]


if settings.DEVELOPMENT == settings.DEVELOPMENT_LOCAL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEVELOPMENT != settings.DEVELOPMENT_PROD:
    urlpatterns += [
        path(
            "api-auth/",
            include("rest_framework.urls", namespace="rest_framework"),
        ),
    ]
