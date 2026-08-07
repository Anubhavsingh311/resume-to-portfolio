from .exceptions import ValidationError


class ResponseValidator:

    REQUIRED_FIELDS = [

        "html",

        "css",

        "js"

    ]

    @classmethod
    def validate(cls, data):

        for field in cls.REQUIRED_FIELDS:

            if field not in data:

                raise ValidationError(
                    f"{field} is missing"
                )

            if not isinstance(data[field], str):

                raise ValidationError(
                    f"{field} must be string"
                )

        return True