"""Contains the API key authentication class."""

from os import getenv

from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from ninja.security import APIKeyHeader

from authentication.database.user_repository import is_user_authenticated
from authentication.models import ApiClient


class ApiKey(APIKeyHeader):
    """API key authentication class."""

    param_name = "X-API-Key"

    @sync_to_async
    def is_authenticated(self, request: HttpRequest) -> bool:
        """Check if the user is authenticated."""
        return is_user_authenticated(request.user)

    async def authenticate(
        self, request: HttpRequest, key: str | None
    ) -> ApiClient | AnonymousUser | None:
        """Authenticate the user."""
        if getenv("TESTS_ENVIRONMENT", "False").lower() == "true":
            return AnonymousUser()

        if not await self.is_authenticated(request):
            return None

        if key is None:
            return None

        try:
            client = await ApiClient.objects.aget(user=request.user)
            if check_password(key, client.client_secret):
                return client
            return None
        except ApiClient.DoesNotExist:
            return None
