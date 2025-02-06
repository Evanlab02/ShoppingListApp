"""Contains the output schemas for the authentication app."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)


class GeneralResponse(Schema):
    """The schema for a general response."""

    message: str
    detail: str


class TokenResponse(Schema):
    """The schema for a token response."""

    token: str
    secret: str
