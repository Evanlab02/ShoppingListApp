"""Contains the API token authentication class."""

import logging
from os import getenv

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from ninja.security import APIKeyHeader

from authentication.models import ApiClient

log = logging.getLogger(__name__)


class ApiToken(APIKeyHeader):
    """API Token authentication class."""

    param_name = "X-API-Token"

    async def authenticate(
        self, request: HttpRequest, key: str | None
    ) -> ApiClient | AnonymousUser | None:
        """Authenticate the user."""
        if getenv("TESTS_ENVIRONMENT", "False").lower() == "true":
            return AnonymousUser()

        if key is None:
            return None

        try:
            client = await ApiClient.objects.aget(token=key)
            return client
        except ApiClient.DoesNotExist:
            return None
