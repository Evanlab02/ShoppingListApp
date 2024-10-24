"""Contains the api user service functions."""

import logging

from django.contrib.auth import aauthenticate
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

from authentication.database.user_repository import (
    create_user,
    does_email_exist,
    does_username_exist,
    is_user_authenticated,
    login_user,
    logout_user,
)
from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.schemas.input import NewUser
from authentication.schemas.output import GeneralResponse

log = logging.getLogger(__name__)
log.info("Authentication API user service loading...")


async def login(request: HttpRequest, username: str, password: str) -> GeneralResponse:
    """
    Login a user.

    Args:
        request (HttpRequest): The request.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        GeneralResponse: The general response.
    """
    log.info("Checking if user is logged in...")
    request_user = await request.auser()
    if is_user_authenticated(request_user):
        log.warning("User already logged in.")
        raise UserAlreadyLoggedIn()

    log.info("Checking user credentials...")
    user = await aauthenticate(request=request, username=username, password=password)
    if user is None:
        log.warning("CRITICAL - Invalid credentials provided for user!")
        raise InvalidCredentials()

    log.info("Logging in...")
    await login_user(request, user)
    return GeneralResponse(message="User successfully logged in.", detail="")


async def logout(request: HttpRequest) -> GeneralResponse:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request.

    Returns:
        GeneralResponse: The general response.
    """
    log.info("Checking if user is logged out...")
    user = await request.auser()
    if not is_user_authenticated(user):
        log.warning("User already logged out.")
        raise UserNotLoggedIn()

    log.info("Logging out...")
    await logout_user(request)
    return GeneralResponse(message="User successfully logged out.", detail="")


async def register_user(
    user: AnonymousUser | AbstractBaseUser | User, new_user: NewUser
) -> GeneralResponse:
    """
    Create a user.

    Args:
        request (HttpRequest): The request.
        new_user (NewUser): The new user.

    Returns:
        GeneralResponse: The general response.
    """
    log.info("Checking if user is logged in...")
    is_authenticated = is_user_authenticated(user)
    if is_authenticated:
        log.warning("User already logged in.")
        raise UserAlreadyLoggedIn()

    log.info("Loading information about new user...")
    username = new_user.username
    password = new_user.password
    password_confirmation = new_user.password_confirmation
    first_name = new_user.first_name
    last_name = new_user.last_name
    email = new_user.email

    log.info("Validating details...")
    if not username or not email or not first_name or not last_name:
        log.warning("Invalid user details.")
        raise InvalidUserDetails()
    elif await does_username_exist(username):
        log.warning("Invalid username.")
        raise UsernameAlreadyExists()
    elif await does_email_exist(email):
        log.warning("Invalid email.")
        raise EmailAlreadyExists()
    elif password != password_confirmation:
        log.warning("Invalid credentials.")
        raise NonMatchingCredentials()

    log.info("Creating user...")
    await create_user(username, password, first_name, last_name, email)
    return GeneralResponse(message="User successfully registered.", detail="")


log.info("Authentication API user service loaded.")
