"""Contains the user repository functions."""

from django.contrib.auth import login, logout
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest


async def create_user(
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
) -> User:
    """
    Create a user.

    Returns:
        int: The user id.
    """
    user = await User.objects.acreate(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    await user.asave()
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


def login_user(request: HttpRequest, user: AbstractBaseUser) -> None:
    """
    Login a user.

    Args:
        request (HttpRequest): The request.
        user (AbstractBaseUser): The user to login.
    """
    login(request, user)


def logout_user(request: HttpRequest) -> None:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request.
    """
    logout(request)
