"""Contains the API key authentication class."""

import logging
from os import getenv

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from ninja.security import APIKeyHeader

from authentication.database.user_repository import is_user_authenticated
from authentication.models import ApiClient

log = logging.getLogger(__name__)
log.info("Loading ninja API key auth...")


class ApiKey(APIKeyHeader):
    """API key authentication class."""

    param_name = "X-API-Key"

    async def authenticate(
        self, request: HttpRequest, key: str | None
    ) -> ApiClient | AnonymousUser | None:
        """Authenticate the user."""
        if getenv("TESTS_ENVIRONMENT", "False").lower() == "true":
            return AnonymousUser()

        user = await request.auser()
        if not is_user_authenticated(user):
            return None

        if key is None:
            return None

        try:
            client = await ApiClient.objects.aget(user=user, is_active=True)
            if check_password(key, client.client_secret):
                return client
            return None
        except ApiClient.DoesNotExist:
            return None


log.info("Loaded ninja API key auth.")
