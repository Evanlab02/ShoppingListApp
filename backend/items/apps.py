"""Contains the items app configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)
log.info("Items app config loading...")


class ItemsConfig(AppConfig):
    """Contains the items app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "items"


log.info("Items app config loaded.")
