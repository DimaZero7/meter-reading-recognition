from django.urls import include, path

from services.api.web.urls import urlpatterns as web_urls

app_name = "api"

urlpatterns = [
    path("web/", include((web_urls, "web"), namespace="web")),
]
