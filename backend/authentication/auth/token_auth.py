"""Contains the API token authentication class."""

import logging

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from ninja.security import APIKeyHeader

from authentication.models import ApiClient

log = logging.getLogger(__name__)


class TokenAuth(APIKeyHeader):
    """API Token authentication class."""

    param_name = "X-API-Token"

    async def authenticate(
        self, request: HttpRequest, key: str | None
    ) -> ApiClient | AnonymousUser | None:
        """Authenticate the user."""
        if key is None:
            return None

        try:
            return await ApiClient.objects.aget(token=key)
        except ApiClient.DoesNotExist:
            return None
