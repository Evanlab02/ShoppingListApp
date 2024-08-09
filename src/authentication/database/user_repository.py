"""Contains the user repository functions."""

import logging

from django.contrib.auth import login, logout
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

log = logging.getLogger(__name__)
log.info("Loading user respository...")


async def create_user(
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
) -> User:
    """
    Create a user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.

    Returns:
        User: The created user.
    """
    user = await User.objects.acreate(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    await user.asave()
    return user


async def does_email_exist(email: str) -> bool:
    """
    Check if a email exists.

    Args:
        email (str): The email of the user.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    email_exists = await User.objects.filter(email=email).aexists()
    return email_exists


async def does_username_exist(username: str) -> bool:
    """
    Check if a username exists.

    Args:
        username (str): The username of the user.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    username_exists = await User.objects.filter(username=username).aexists()
    return username_exists


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


def login_user(request: HttpRequest, user: AbstractBaseUser | User) -> None:
    """
    Login a user.

    Args:
        request (HttpRequest): The request.
        user (AbstractBaseUser | User): The user to login.
    """
    login(request, user)


def logout_user(request: HttpRequest) -> None:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request.
    """
    logout(request)


log.info("Loaded user respository.")
