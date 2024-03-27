REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "COERCE_DECIMAL_TO_STRING": False,
    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    "DATE_FORMAT": "%d.%m.%Y",
}

if DEVELOPMENT != DEVELOPMENT_PROD:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]

if DEVELOPMENT == DEVELOPMENT_LOCAL:
    rest_authentication_classes = REST_FRAMEWORK.get("DEFAULT_AUTHENTICATION_CLASSES", [])

    session_authentication = "rest_framework.authentication.SessionAuthentication"
    basic_authentication = "rest_framework.authentication.BasicAuthentication"

    if session_authentication not in rest_authentication_classes:
        rest_authentication_classes.insert(0, session_authentication)

    if basic_authentication not in rest_authentication_classes:
        rest_authentication_classes.insert(1, basic_authentication)
