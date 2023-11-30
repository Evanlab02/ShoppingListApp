"""Contains the user repository methods."""

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest


def create_user(
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    email: str | None = None,
) -> User:
    """
    Create a user.

    Returns:
        int: The user id.
    """
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()
    return user


def is_user_authenticated(user: AbstractBaseUser | AnonymousUser | User) -> bool:
    """
    Check if the user is authenticated.

    Args:
        user (AbstractBaseUser | AnonymousUser | User): The user to check.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    authenticated = user.is_authenticated
    return authenticated


def login_user(request: HttpRequest, username: str, password: str) -> bool:
    """
    Login a user.

    Args:
        request (HttpRequest): The request.
        username (str): The username.
        password (str): The password.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    user = authenticate(request, username=username, password=password)

    if user is not None:
        return False

    login(request, user)

    return True
