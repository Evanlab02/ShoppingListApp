"""Contains constants for the authentication app."""

# Third party imports
from os import environ

# Set API key parameter
API_KEY_PARAM = environ.get("API_KEY_PARAM", "X-API-Key")

__all__ = ["API_KEY_PARAM"]
