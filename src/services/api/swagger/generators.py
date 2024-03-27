import re

from drf_yasg.inspectors import SwaggerAutoSchema

from services.api.swagger import schemas, status
from services.api.swagger.settings import schema_settings


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def __init__(
        self,
        view,
        path,
        method,
        components,
        request,
        overrides,
        operation_keys=None,
    ):
        super().__init__(
            view, path, method, components, request, overrides, operation_keys
        )

        self.auth_permission_classes_tuple = tuple(
            schema_settings.BASE_AUTH_PERMISSION_CLASSES
        )

    def get_default_response_serializer(self):
        if hasattr(self.view, "response_serializer_class"):
            return self.view.response_serializer_class()

        return super().get_default_response_serializer()

    def get_request_serializer(self):
        if (
            hasattr(self.view, "serializer_class")
            and self.method in self.body_methods
        ):
            request_serializer_class = self.view.serializer_class
            return (
                request_serializer_class()
                if request_serializer_class is not None
                else None
            )

        return super().get_request_serializer()

    def get_responses(self):
        responses = super().get_responses()

        self._add_default_bad_request_response(responses)
        self._add_default_authentication_responses(responses)
        self._add_default_not_found_response(responses)

        return responses

    def _add_default_bad_request_response(self, responses):
        if status.BAD_REQUEST in responses:
            return

        if self.get_request_serializer():
            responses[status.BAD_REQUEST] = schemas.bad_request

    def _add_default_authentication_responses(self, responses):
        # check permissions and if user must be authenticated,
        # add default Unauthorized and Forbidden responses
        permissions = self.view.get_permissions()
        if permissions and schema_settings.BASE_AUTH_PERMISSION_CLASSES:
            for permission in permissions:
                if isinstance(permission, self.auth_permission_classes_tuple):
                    if status.UNAUTHORIZED not in responses:
                        responses[status.UNAUTHORIZED] = schemas.unauthorized

                    if status.FORBIDDEN not in responses:
                        responses[status.FORBIDDEN] = schemas.forbidden

                    break

    def _add_default_not_found_response(self, responses):
        # if there is in_path params, it means that this is details view and
        # it could return 404 NOT_FOUND response.
        if status.NOT_FOUND not in responses and re.search(
            r"/{\w+}/", self.path
        ):
            responses[status.NOT_FOUND] = schemas.not_found
