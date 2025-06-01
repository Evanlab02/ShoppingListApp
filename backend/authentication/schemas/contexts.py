"""Contains context schemas for the authentication app."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)


class BaseContext(Schema):
    """Base context schema."""

    error: str | None = None


class TokenContext(BaseContext):
    """Token context schema."""

    token: str | None = None
