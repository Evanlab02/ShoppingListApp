"""Contains views for the authentication app."""


from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators import async_login_required, login_required
from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
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


@require_http_methods(["POST"])
@login_required
def logout_action(request: HttpRequest) -> HttpResponse:
    """
    Handle the logout action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    logout(request)
    return HttpResponseRedirect(f"/{LOGIN_ROUTE}")


@require_http_methods(["GET"])
@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Render the logout view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    context = get_logout_view_context(request)
    return render(request, "auth/logout.html", context.model_dump())


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


@require_http_methods(["GET"])
@login_required
def confirm_token(request: HttpRequest) -> HttpResponse:
    """
    Handle the register view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
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
    user = request.user
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
    user = request.user
    context = await disable_client(user)
    return render(request, "auth/disable-token.html", context.model_dump())
