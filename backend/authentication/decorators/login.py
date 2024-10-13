"""Contains decorators for the authentication app."""

import logging
from typing import Any

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponseRedirect

from authentication.database.user_repository import is_user_authenticated

log = logging.getLogger(__name__)
log.info("Loading login decorators...")


def login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = is_user_authenticated(user)
        if not is_authenticated:
            return HttpResponseRedirect("/?error=You must be logged in to access that page.")
        else:
            return function(request, *args, **kw)

    return wrapper


def async_login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    async def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = await request.auser()
        is_authenticated = is_user_authenticated(user)
        if not is_authenticated:
            return HttpResponseRedirect("/?error=You must be logged in to access that page.")
        else:
            return await function(request, *args, **kw)

    return wrapper


def redirect_if_logged_in(function: Any) -> Any:
    """Redirects user to dashboard page if logged in."""

    def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = is_user_authenticated(user)
        if is_authenticated:
            return HttpResponseRedirect("/shopping/dashboard/")
        else:
            return function(request, *args, **kw)

    return wrapper


def async_redirect_if_logged_in(function: Any) -> Any:
    """Redirects user to dashboard page if logged in."""

    async def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = await request.auser()
        is_authenticated = await sync_to_async(is_user_authenticated)(user)
        if is_authenticated:
            return HttpResponseRedirect("/shopping/dashboard/")
        else:
            return await function(request, *args, **kw)

    return wrapper


log.info("Loaded login decorators.")
