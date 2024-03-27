from django.urls import include, path

from services.api.swagger.views import LoginRequiredWebSchemaView
from services.api.web.training_set import urls as training_set_urls

app_name = "web"

urlpatterns = [
    path("swagger.yaml", LoginRequiredWebSchemaView.without_ui()),
    path(
        "swagger/",
        LoginRequiredWebSchemaView.with_ui("swagger", cache_timeout=0),
    ),
    path(
        "training-set/",
        include(
            (training_set_urls.urlpatterns, training_set_urls.app_name),
            namespace="training_set",
        ),
    ),
    path(
        "none/",
        include(
            (training_set_urls.urlpatterns, training_set_urls.app_name),
            namespace="none",
        ),
    ),
]
