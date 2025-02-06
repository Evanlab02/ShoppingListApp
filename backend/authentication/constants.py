"""Contains constants for the authentication app."""

import logging

log = logging.getLogger(__name__)

INPUT_MAPPING = {
    "username-input": "username",
    "email-input": "email",
    "first-name-input": "first_name",
    "last-name-input": "last_name",
    "password-confirm-input": "password_confirm",
    "password-input": "password",
    "submit-login": "submit",
    "submit-register": "submit",
    "submit-logout": "submit",
    "submit-cancel": "cancel",
}
