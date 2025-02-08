"""Contains the dashboard application configuration."""

import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class DashboardConfig(AppConfig):
    """Dashboard application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
