"""Contains the stores app configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class StoresConfig(AppConfig):
    """Stores app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "stores"
