"""Contains decorators for the authentication app."""

from typing import Any

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponseRedirect

from authentication.database.user_repository import is_user_authenticated


def login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = is_user_authenticated(user)
        if not is_authenticated:
            return HttpResponseRedirect(
                "/?error=You must be logged in to access that page."
            )
        else:
            return function(request, *args, **kw)

    return wrapper


def async_login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    async def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = await sync_to_async(is_user_authenticated)(user)
        if not is_authenticated:
            return HttpResponseRedirect(
                "/?error=You must be logged in to access that page."
            )
        else:
            return await function(request, *args, **kw)

    return wrapper
