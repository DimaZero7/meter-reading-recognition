from django.utils.translation import gettext_lazy as _

from apps.common.exceptions import CustomMessageException


class NotEnoughElementsException(CustomMessageException):
    custom_message = _("there are not enough elements to generate images")


class MaxOptionsException(CustomMessageException):
    pass
