"""Contains the API key cookie authentication classes."""

from typing import Any, Optional

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import HttpRequest
from ninja.security.apikey import APIKeyCookie


class SessionAuth(APIKeyCookie):
    "Reusing Django session authentication"

    param_name: str = settings.SESSION_COOKIE_NAME

    @sync_to_async
    def _is_authenticated(self, request: HttpRequest) -> bool:
        return request.user.is_authenticated

    async def authenticate(
        self, request: HttpRequest, key: Optional[str]
    ) -> Optional[Any]:
        if await self._is_authenticated(request):
            return request.user

        return None
