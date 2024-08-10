"""Contains the authentication app configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)
log.info("Authentication config loading...")


class AuthenticationConfig(AppConfig):
    """Contains the authentication app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"


log.info("Authentication config loaded.")
