"""Contains decorators for the authentication app."""

from .login import async_login_required, login_required

__all__ = ["async_login_required", "login_required"]
