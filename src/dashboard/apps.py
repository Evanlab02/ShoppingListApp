"""Contains the dashboard application configuration."""

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Dashboard application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
