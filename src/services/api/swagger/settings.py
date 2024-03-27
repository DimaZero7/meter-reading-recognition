from drf_yasg.app_settings import AppSettings

AUTO_SCHEMA_DEFAULTS = {
    "BASE_AUTH_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
}

IMPORT_STRINGS = [
    "BASE_AUTH_PERMISSION_CLASSES",
]


schema_settings = AppSettings(
    "AUTO_SCHEMA_SETTINGS", AUTO_SCHEMA_DEFAULTS, IMPORT_STRINGS
)
