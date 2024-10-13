"""Contains views for the authentication app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators import async_login_required, async_redirect_if_logged_in
from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UsernameAlreadyExists,
)
from authentication.services.views.client_service import disable_client, enable_client
from authentication.services.views.user_service import (
    get_login_view_context,
    get_logout_view_context,
    get_register_page_context,
    login,
    logout,
    register_user,
)

DASHBOARD_ROUTE = "shopping/dashboard/"
LOGOUT_ROUTE = "logout"
LOGOUT_ACTION_ROUTE = "action/logout"
LOGIN_ROUTE = ""
LOGIN_ACTION_ROUTE = "action/login"
REGISTER_ROUTE = "register"
REGISTER_ACTION_ROUTE = "action/register"
CONFIRM_TOKEN_ROUTE = "token"
ENABLE_CLIENT_ROUTE = "token/register"
DISABLE_CLIENT_ROUTE = "token/disable"

log = logging.getLogger(__name__)
log.info("Auth Views loading...")


@require_http_methods(["POST"])
@async_redirect_if_logged_in
async def login_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the login action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to login.")
    try:
        await login(request)
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")
    except InvalidCredentials as error:
        log.warning(f"Error with login: {error}")
        return HttpResponseRedirect(f"/{LOGIN_ROUTE}?error={error}")


@require_http_methods(["GET"])
@async_redirect_if_logged_in
async def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the login view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to view login page.")
    context = await get_login_view_context(request)
    return render(request, "auth/index.html", context.model_dump())


@require_http_methods(["POST"])
@async_login_required
async def logout_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the logout action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to logout.")
    await logout(request)
    return HttpResponseRedirect(f"/{LOGIN_ROUTE}")


@require_http_methods(["GET"])
@async_login_required
async def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Render the logout view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to view logout page.")
    context = await get_logout_view_context(request)
    return render(request, "auth/logout.html", context.model_dump())


@require_http_methods(["POST"])
@async_redirect_if_logged_in
async def register_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the register action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to register a user.")
    try:
        await register_user(request)
        return HttpResponseRedirect(f"/{LOGIN_ROUTE}")
    except (
        InvalidUserDetails,
        NonMatchingCredentials,
        UsernameAlreadyExists,
        EmailAlreadyExists,
    ) as error:
        log.warning(f"Registration error: {error}")
        return HttpResponseRedirect(f"/{REGISTER_ROUTE}?error={error}")


@require_http_methods(["GET"])
@async_redirect_if_logged_in
async def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to view register page.")
    context = await get_register_page_context(request)
    return render(request, "auth/register.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def confirm_token(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to get token landing page.")
    return render(request, "auth/confirm_token.html", {})


@require_http_methods(["GET"])
@async_login_required
async def enable_api_client(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to enable API client.")
    user = await request.auser()
    context = await enable_client(user)
    return render(request, "auth/token.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def disable_api_client(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    log.info("Retrieved request to disable API client.")
    user = await request.auser()
    context = await disable_client(user)
    return render(request, "auth/disable-token.html", context.model_dump())


log.info("Auth Views loaded.")
