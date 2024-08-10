"""Contains the stores app configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)
log.info("Stores app config loading...")


class StoresConfig(AppConfig):
    """Stores app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "stores"


log.info("Stores app config loaded.")
