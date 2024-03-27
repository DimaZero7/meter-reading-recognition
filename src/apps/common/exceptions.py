from typing import Optional


class CustomMessageException(Exception):
    custom_message = None

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.custom_message)
