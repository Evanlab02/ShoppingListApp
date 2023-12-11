"""Contains views for the authentication app."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.services.views.user_service import (
    get_login_view_context,
    get_logout_view_context,
    get_register_page_context,
    login,
    register_user,
)

DASHBOARD_ROUTE = "shopping/dashboard/"
LOGOUT_ROUTE = "logout"
LOGIN_ROUTE = ""
LOGIN_ACTION_ROUTE = "action/login"
REGISTER_ROUTE = "register"
REGISTER_ACTION_ROUTE = "action/register"


@require_http_methods(["POST"])
def login_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the login action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        login(request)
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")
    except UserAlreadyLoggedIn:
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")
    except InvalidCredentials as error:
        return HttpResponseRedirect(f"/{LOGIN_ROUTE}?error={error}")


@require_http_methods(["GET"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the login view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        context = get_login_view_context(request)
        return render(request, "auth/index.html", context.model_dump())
    except UserAlreadyLoggedIn:
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")


@require_http_methods(["GET"])
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Render the logout view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        context = get_logout_view_context(request)
        return render(request, "auth/logout.html", context.model_dump())
    except UserNotLoggedIn as error:
        return HttpResponseRedirect(f"/{LOGIN_ROUTE}?error={error}")


@require_http_methods(["POST"])
async def register_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the register action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        await register_user(request)
        return HttpResponseRedirect(f"/{LOGIN_ROUTE}")
    except UserAlreadyLoggedIn:
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")
    except (
        InvalidUserDetails,
        NonMatchingCredentials,
        UsernameAlreadyExists,
        EmailAlreadyExists,
    ) as error:
        return HttpResponseRedirect(f"/{REGISTER_ROUTE}?error={error}")


@require_http_methods(["GET"])
def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        context = get_register_page_context(request)
        return render(request, "auth/register.html", context.model_dump())
    except UserAlreadyLoggedIn:
        return HttpResponseRedirect(f"/{DASHBOARD_ROUTE}")
