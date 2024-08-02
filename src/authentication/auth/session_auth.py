"""Contains the session authentication class."""

import logging
from typing import Any, Optional

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import HttpRequest
from ninja.security.apikey import APIKeyCookie

from authentication.database.user_repository import is_user_authenticated

log = logging.getLogger(__name__)
log.info("Loading ninja session auth...")


class SessionAuth(APIKeyCookie):
    """Reusing Django session authentication."""

    param_name: str = settings.SESSION_COOKIE_NAME

    @sync_to_async
    def is_authenticated(self, request: HttpRequest) -> bool:
        """Check if the user is authenticated."""
        return is_user_authenticated(request.user)

    async def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        """Authenticate the user."""
        if await self.is_authenticated(request):
            return request.user

        return None


log.info("Loaded ninja session auth.")
