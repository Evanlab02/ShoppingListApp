"""Contains views for the authentication app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from authentication.decorators import async_login_required, async_redirect_if_logged_in
from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UsernameAlreadyExists,
)
from authentication.services.views.user_service import UserService

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
service = UserService()


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
    try:
        await service.login(request)
        return HttpResponseRedirect(reverse("dashboard"))
    except InvalidCredentials as error:
        log.warning(f"Error with login: {error}")
        return HttpResponseRedirect(f"{reverse('login_page')}?error={error}")


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
    context = await service.get_login_view_context(request)
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
    await service.logout(request)
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
    context = await service.get_logout_view_context(request)
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
    try:
        await service.register_user(request)
        return HttpResponseRedirect(reverse("login_page"))
    except (
        InvalidUserDetails,
        NonMatchingCredentials,
        UsernameAlreadyExists,
        EmailAlreadyExists,
    ) as error:
        log.warning(f"Registration error: {error}")
        return HttpResponseRedirect(f"{reverse('register_page')}?error={error}")


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
    context = await service.get_register_page_context(request)
    return render(request, "auth/register.html", context.model_dump())
