from typing import Iterable, Type

from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper


class ValidationError(RequestValidationError):
    """Class-wrapper for easily usage of basic RequestValidationError class"""

    def __init__(
        self,
        message: str,
        location: Iterable[str] | str = None,
        location_root: str = "body",
        error_class: Type[Exception] = ValueError,
    ):
        if location is None:
            location = tuple()
        if isinstance(location, str):
            location = (location,)

        super().__init__([ErrorWrapper(error_class(message), (location_root, *location))])
