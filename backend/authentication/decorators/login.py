"""Contains decorators for the authentication app."""

import logging
from typing import Any

from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from authentication.database.user_repo import UserRepository

log = logging.getLogger(__name__)
repo = UserRepository()


def login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = repo.is_user_authenticated(user)
        if not is_authenticated:
            return HttpResponseRedirect(reverse("login_page") + "?error=You must be logged in to access that page.")
        else:
            return function(request, *args, **kw)

    return wrapper


def async_login_required(function: Any) -> Any:
    """Enforces user to be logged in."""

    async def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = await request.auser()
        is_authenticated = repo.is_user_authenticated(user)
        if not is_authenticated:
            return HttpResponseRedirect(reverse("login_page") + "?error=You must be logged in to access that page.")
        else:
            return await function(request, *args, **kw)

    return wrapper


def redirect_if_logged_in(function: Any) -> Any:
    """Redirects user to dashboard page if logged in."""

    def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = request.user
        is_authenticated = repo.is_user_authenticated(user)
        if is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return function(request, *args, **kw)

    return wrapper


def async_redirect_if_logged_in(function: Any) -> Any:
    """Redirects user to dashboard page if logged in."""

    async def wrapper(request: HttpRequest, *args: Any, **kw: Any) -> Any:
        """Wrap around child function."""
        user = await request.auser()
        is_authenticated = repo.is_user_authenticated(user)
        if is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return await function(request, *args, **kw)

    return wrapper
