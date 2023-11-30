"""Contains the user repository methods."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User


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
