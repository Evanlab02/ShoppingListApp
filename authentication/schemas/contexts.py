"""Contains context schemas for the authentication app."""

from ninja import Schema


class BaseContext(Schema):
    """Base context schema."""

    error: str | None = None


class LoginContext(BaseContext):
    """Login context schema."""

    username_input: str = "username-input"
    password_input: str = "password-input"
    submit_login: str = "submit-login"
