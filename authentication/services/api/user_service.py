"""Contains the api user service functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database.user_repository import (
    create_user,
    does_email_exist,
    does_username_exist,
    is_user_authenticated,
)
from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
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
    if is_user_authenticated(user):
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
