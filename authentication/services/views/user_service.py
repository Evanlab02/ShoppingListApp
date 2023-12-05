"""Contains view user service functions."""

from django.http import HttpRequest

from authentication.database.user_repository import is_user_authenticated
from authentication.errors.api_exceptions import UserAlreadyLoggedIn
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
    return LoginContext(error=error)
