from pydantic.types import ConstrainedStr

from app.users import errors


class Username(ConstrainedStr):
    min_length = 4
    max_length = 32

    @classmethod
    def validate(cls, value: str) -> str:
        value = super().validate(value)

        for symbol in value:
            if not symbol.isalnum() and not symbol in ["_", ".", "-"]:
                raise ValueError(errors.INVALID_USERNAME_FORMAT)

        return value


class Password(ConstrainedStr):
    min_length = 6
    max_length = 256

    @classmethod
    def validate(cls, value: str) -> str:
        value = super().validate(value)

        has_number, has_uppercase = False, False

        for symbol in value:
            if not has_number and symbol.isnumeric():
                has_number = True
            if not has_uppercase and symbol.isupper():
                has_uppercase = True

        if not (has_uppercase and has_number):
            raise ValueError()

        return value
