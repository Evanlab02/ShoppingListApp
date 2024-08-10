"""Contains decorators for the authentication app."""

import logging

from .login import (
    async_login_required,
    async_redirect_if_logged_in,
    login_required,
    redirect_if_logged_in,
)

log = logging.getLogger(__name__)
log.info("Loading auth decorators...")

__all__ = [
    "async_login_required",
    "login_required",
    "redirect_if_logged_in",
    "async_redirect_if_logged_in",
]
