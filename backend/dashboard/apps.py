"""Contains the dashboard application configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)
log.info("Dashboard app config loading...")


class DashboardConfig(AppConfig):
    """Dashboard application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"


log.info("Dashboard app config loaded.")
