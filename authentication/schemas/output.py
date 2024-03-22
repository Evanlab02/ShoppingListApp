"""Contains the output schemas for the authentication app."""

from ninja import Schema


class GeneralResponse(Schema):
    """The schema for a general response."""

    message: str
    detail: str
