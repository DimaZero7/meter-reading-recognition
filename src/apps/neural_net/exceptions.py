from apps.common.exceptions import CustomMessageException


class NumberIsoLongException(CustomMessageException):
    custom_message = "number greater than 11 characters"
