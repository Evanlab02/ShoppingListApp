"""Contains the API token authentication class."""

import logging
from datetime import datetime

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
            client = await ApiClient.objects.aget(token=key)
            if datetime.now().timestamp() > client.token_expiration:
                return None
            return client
        except ApiClient.DoesNotExist:
            return None
