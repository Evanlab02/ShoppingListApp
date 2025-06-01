"""Contains the session authentication class."""

import logging
from typing import Any, Optional

from django.conf import settings
from django.http import HttpRequest
from ninja.security.apikey import APIKeyCookie

from authentication.database.user_repo import UserRepository

log = logging.getLogger(__name__)
repo = UserRepository()


class SessionAuth(APIKeyCookie):
    """Reusing Django session authentication."""

    param_name: str = settings.SESSION_COOKIE_NAME

    async def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        """Authenticate the user."""
        user = await request.auser()
        if repo.is_user_authenticated(user):
            return user

        return None
