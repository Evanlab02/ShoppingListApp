"""Contains auth models for the routers."""

import logging

from authentication.auth.session_auth import SessionAuth
from authentication.auth.token_auth import TokenAuth

log = logging.getLogger(__name__)

SESSION_AUTH = SessionAuth()
TOKEN_AUTH = TokenAuth()
