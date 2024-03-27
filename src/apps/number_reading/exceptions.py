from django.utils.translation import gettext_lazy as _

from apps.common.exceptions import CustomMessageException


class NumberIsoLongException(CustomMessageException):
    custom_message = _("number greater than 11 characters")
