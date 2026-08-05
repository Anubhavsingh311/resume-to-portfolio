class ParserError(Exception):
    """Base parser exception."""
    pass


class InvalidJSON(ParserError):
    pass


class ValidationError(ParserError):
    pass