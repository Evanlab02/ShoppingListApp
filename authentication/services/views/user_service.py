"""Contains view user service functions."""

from django.contrib.auth import authenticate
from django.http import HttpRequest

from authentication.constants import INPUT_MAPPING
from authentication.database.user_repository import is_user_authenticated, login_user
from authentication.errors.api_exceptions import InvalidCredentials, UserAlreadyLoggedIn
from authentication.schemas.contexts import LoginContext


def get_login_view_context(request: HttpRequest) -> LoginContext:
    """
    Generate context for the login view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        LoginContext: The context for the login view.
    """
    if is_user_authenticated(request.user):
        raise UserAlreadyLoggedIn()

    error = request.GET.get("error")
    username_input = INPUT_MAPPING.get("username-input", "username-input")
    password_input = INPUT_MAPPING.get("password-input", "password-input")
    submit_login = INPUT_MAPPING.get("submit-login", "submit-login")

    return LoginContext(
        error=error,
        username_input=username_input,
        password_input=password_input,
        submit_login=submit_login,
    )


def login(request: HttpRequest) -> None:
    """
    Log in the user.

    Args:
        request (HttpRequest): The request object.
    """
    if is_user_authenticated(request.user):
        raise UserAlreadyLoggedIn()

    username_input = INPUT_MAPPING.get("username-input", "username-input")
    password_input = INPUT_MAPPING.get("password-input", "password-input")
    username = request.POST.get(username_input)
    password = request.POST.get(password_input)

    user = authenticate(request=request, username=username, password=password)
    if user is None:
        raise InvalidCredentials()

    login_user(request, user)
