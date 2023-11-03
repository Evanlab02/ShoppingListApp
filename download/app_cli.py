"""Contains the main typer CLI app for the shopping app CLI."""

from api.github import (
    download_app_release,
    download_backend_release,
    download_frontend_release,
)


def install():
    """Install the shopping app."""
    download_app_release()
    download_frontend_release()
    download_backend_release()
