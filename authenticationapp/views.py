"""Contains views for the authentication app."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .database import UserRepository

USER_REPOSITORY = UserRepository()
DASHBOARD_ROUTE = "/shopping/dashboard/"


@require_http_methods(["GET"])
def login_page(request: HttpRequest) -> HttpResponse:
    """
    Render the login page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered login page.
    """
    if USER_REPOSITORY.is_authenticated(request.user):
        return HttpResponseRedirect("/shopping/dashboard/")

    error = request.GET.get("error")
    return render(request, "auth/index.html", {"error": error})


@require_http_methods(["POST"])
def login_action(request: HttpRequest) -> HttpResponseRedirect:
    """
    Log the user in.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponsePermanentRedirect: Redirects the user to the dashboard or the error page.
    """
    if USER_REPOSITORY.is_authenticated(request.user):
        return HttpResponseRedirect("/?error='Already logged in.'")

    username = request.POST.get("username-input")
    password = request.POST.get("password-input")
    successful_login = USER_REPOSITORY.login_user(request, username, password)

    if successful_login:
        return HttpResponseRedirect(DASHBOARD_ROUTE)

    return HttpResponseRedirect("/?error='Invalid credentials.'")


@login_required(login_url="/", redirect_field_name=None)
@require_http_methods(["GET"])
def logout_page(request: HttpRequest) -> HttpResponse:
    """
    Log the user out.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered logout page.
    """
    return render(request, "auth/logout.html")


@login_required(login_url="/", redirect_field_name=None)
@require_http_methods(["POST"])
def logout_action(request: HttpRequest) -> HttpResponseRedirect:
    """
    Log the user out.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponsePermanentRedirect: Redirects the user to the login page.
    """
    successful_logout = USER_REPOSITORY.logout_user(request)
    error = ""

    if not successful_logout:
        error = "Unexpected error when logging out, please try again."

    error_param = "" if not error else f"?error='{error}'"

    return HttpResponseRedirect(f"/{error_param}")


@require_http_methods(["GET"])
def register_page(request: HttpRequest):
    """
    Render the register page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponsePermanentRedirect: Redirects the user to the dashboard.
        HttpResponse: The rendered register page.
    """
    error = request.GET.get("error")
    return render(request, "auth/register.html", {"error": error})


@require_http_methods(["POST"])
def register_action(request: HttpRequest) -> HttpResponseRedirect:
    """
    Register a new user.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponsePermanentRedirect: Redirects the user to the dashboard or the error page.
    """
    if USER_REPOSITORY.is_authenticated(request.user):
        return HttpResponseRedirect("/?error='Already logged in.'")

    username = request.POST.get("username-input")
    password = request.POST.get("password-input")
    confirm_password = request.POST.get("confirm-password-input")
    first_name = request.POST.get("first-name-input")
    last_name = request.POST.get("last-name-input")

    # Need to make it none, otherwise empty strings get registered as an email
    email = request.POST.get("email-input")
    email = None if not email else email

    if not username and not password and not confirm_password:
        return HttpResponseRedirect(
            "/register?error='Please fill in all required fields.'"
        )
    elif password != confirm_password:
        return HttpResponseRedirect("/register?error='Passwords do not match.'")
    elif User.objects.filter(username=username).exists():
        return HttpResponseRedirect("/register?error='Username already exists.'")
    elif User.objects.filter(email=email).exists():
        return HttpResponseRedirect("/register?error='Email already exists.'")

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()

    return HttpResponseRedirect("/")
