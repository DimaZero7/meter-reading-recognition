from drf_yasg import openapi
from rest_framework.settings import api_settings

bad_request = openapi.Response(
    "Validation Error Response",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
                description=(
                    "List of validation errors not related " "to any field"
                ),
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
            ),
        },
        additional_properties=openapi.Schema(
            description=(
                "A list of error messages for each field "
                "that triggered a validation error"
            ),
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
        ),
    ),
)


unauthorized = openapi.Response(
    (
        "Unauthorized Response. Authentication credentials were not"
        " provided or access token was expired."
    ),
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="User is not authorized",
            ),
        },
    ),
)


forbidden = openapi.Response(
    "User is authenticated, but not authorized to perform this action",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="You do not have permission to perform this action.",  # noqa: E501
            ),
        },
    ),
)


not_found = openapi.Response(
    "Invalid pk or object not found due to search filter",
)


conflict = openapi.Response(
    (
        "Validation error that not related to client request data, "
        "but to some interanal business logic or restrictions"
    ),
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "non_field_errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
            ),
        },
    ),
)
