from django.db.models import Choices
from drf_yasg.inspectors.base import NotHandled
from drf_yasg.inspectors.field import ChoiceFieldInspector


class EnumWithDescriptionFieldInspector(ChoiceFieldInspector):
    def field_to_swagger_object(
        self, field, swagger_object_type, use_references, **kwargs
    ):
        result = super().field_to_swagger_object(
            field, swagger_object_type, use_references, **kwargs
        )
        if result == NotHandled:
            return result

        result.description = self._get_choices_description(field)
        return result

    def _get_choices_description(self, field):
        description = "Possible values:\n\n"
        for value, label in field.choices.items():
            if isinstance(value, Choices):
                description += f"{value} - {value.label}\n"
            else:
                description += f"{value} - {label}\n"
        return description
