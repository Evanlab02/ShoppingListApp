"""Contains context schemas for the authentication app."""

from ninja import Schema


class LoginContext(Schema):
    """Login context schema."""

    error: str | None = None
