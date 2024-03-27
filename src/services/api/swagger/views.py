from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


class WebPrivateAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = "/api/web/"
        return schema


web_schema_view = get_schema_view(
    openapi.Info(
        title="Web API documentation",
        default_version="v1",
        description="Web API annotation",
    ),
    urlconf="services.api.web.urls",
    generator_class=WebPrivateAPISchemeGenerator,
    public=True,
    permission_classes=(AllowAny,),
)


class LoginRequiredWebSchemaView(LoginRequiredMixin, web_schema_view):
    login_url = settings.SWAGGER_SETTINGS["LOGIN_URL"]
