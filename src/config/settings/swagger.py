from django.urls import reverse_lazy

SWAGGER_SETTINGS = {
    "LOGIN_URL": reverse_lazy("rest_framework:login"),
    "LOGOUT_URL": reverse_lazy("rest_framework:logout"),
    "USE_SESSION_AUTH": False,
    "DEFAULT_AUTO_SCHEMA_CLASS": "services.api.swagger.generators.CustomSwaggerAutoSchema",
    "EXCLUDED_MEDIA_TYPES": [],
    # override default field inspectors
    # to use custom field inspector for enum fields
    "DEFAULT_FIELD_INSPECTORS": [
        "drf_yasg.inspectors.CamelCaseJSONFilter",
        "drf_yasg.inspectors.RecursiveFieldInspector",
        "drf_yasg.inspectors.ReferencingSerializerInspector",
        "services.api.swagger.inspectors.EnumWithDescriptionFieldInspector",
        "drf_yasg.inspectors.FileFieldInspector",
        "drf_yasg.inspectors.DictFieldInspector",
        "drf_yasg.inspectors.JSONFieldInspector",
        "drf_yasg.inspectors.HiddenFieldInspector",
        "drf_yasg.inspectors.RelatedFieldInspector",
        "drf_yasg.inspectors.SerializerMethodFieldInspector",
        "drf_yasg.inspectors.SimpleFieldInspector",
        "drf_yasg.inspectors.StringDefaultFieldInspector",
    ],
}
