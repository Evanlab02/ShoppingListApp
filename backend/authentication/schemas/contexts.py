"""Contains context schemas for the authentication app."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)
log.info("Loading authentication contexts...")


class BaseContext(Schema):
    """Base context schema."""

    error: str | None = None


class LoginContext(BaseContext):
    """Login context schema."""

    username_input: str = "username-input"
    password_input: str = "password-input"
    submit_login: str = "submit-login"


class RegisterContext(BaseContext):
    """Register context schema."""

    username_input: str = "username-input"
    email_input: str = "email-input"
    first_name_input: str = "first-name-input"
    last_name_input: str = "last-name-input"
    password_input: str = "password-input"
    password_confirm_input: str = "password-confirm-input"
    submit_register: str = "submit-register"


class LogoutContext(BaseContext):
    """Logout context schema."""

    submit_logout: str = "submit-logout"
    submit_cancel: str = "submit-cancel"
    dashboard_route: str = "/shopping/dashboard/"


class TokenContext(BaseContext):
    """Token context schema."""

    token: str | None = None


log.info("Loaded authentication contexts.")
