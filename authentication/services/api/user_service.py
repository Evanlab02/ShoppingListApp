"""Contains the api user service functions."""

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

from authentication.database.user_repository import (
    create_user,
    does_email_exist,
    does_username_exist,
    get_csrf_token,
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
    is_authenticated = await sync_to_async(is_user_authenticated)(user)
    if is_authenticated:
        raise UserAlreadyLoggedIn()

    username = new_user.username
    password = new_user.password
    password_confirmation = new_user.password_confirmation
    first_name = new_user.first_name
    last_name = new_user.last_name
    email = new_user.email

    if not username or not email or not first_name or not last_name:
        raise InvalidUserDetails()
    elif await does_username_exist(username):
        raise UsernameAlreadyExists()
    elif await does_email_exist(email):
        raise EmailAlreadyExists()
    elif password != password_confirmation:
        raise NonMatchingCredentials()

    await create_user(username, password, first_name, last_name, email)

    return GeneralResponse(message="User successfully registered.", detail="")


def login(request: HttpRequest, username: str, password: str) -> GeneralResponse:
    """
    Login a user.

    Args:
        request (HttpRequest): The request.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        GeneralResponse: The general response.
    """
    if is_user_authenticated(request.user):
        raise UserAlreadyLoggedIn()

    user = authenticate(request=request, username=username, password=password)
    if user is None:
        raise InvalidCredentials()

    login_user(request, user)
    return GeneralResponse(message="User successfully logged in.", detail="")


def logout(request: HttpRequest) -> GeneralResponse:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request.

    Returns:
        GeneralResponse: The general response.
    """
    if not is_user_authenticated(request.user):
        raise UserNotLoggedIn()

    logout_user(request)
    return GeneralResponse(message="User successfully logged out.", detail="")


def get_token(request: HttpRequest) -> GeneralResponse:
    """
    Get the CSRF token.

    Args:
        request (HttpRequest): The request.

    Returns:
        GeneralResponse: The general response.
    """
    token = get_csrf_token(request)
    return GeneralResponse(message="Token successfully retrieved.", detail=token)
