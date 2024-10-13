"""Contains view user service functions."""

import logging

from django.contrib.auth import aauthenticate
from django.http import HttpRequest

from authentication.constants import INPUT_MAPPING
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
from authentication.schemas.contexts import LoginContext, LogoutContext, RegisterContext

log = logging.getLogger(__name__)
log.info("Authentication View user service loading...")

LOADING_REQUEST = "Loading request info..."
CHECKING_USER_LOGGED_IN = "Checking if user is logged in..."
USER_ALREADY_LOGGED_IN = "User is already logged in."


async def get_login_view_context(request: HttpRequest) -> LoginContext:
    """
    Generate context for the login view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        LoginContext: The context for the login view.
    """
    log.info(CHECKING_USER_LOGGED_IN)
    user = await request.auser()
    if is_user_authenticated(user):
        log.warning(USER_ALREADY_LOGGED_IN)
        raise UserAlreadyLoggedIn()

    log.info(LOADING_REQUEST)
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


async def get_logout_view_context(request: HttpRequest) -> LogoutContext:
    """
    Generate context for the logout view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        LogoutContext: The context for the logout view.
    """
    log.info("Checking if user is logged out...")
    user = await request.auser()
    if not is_user_authenticated(user):
        log.warning("User is already logged out.")
        raise UserNotLoggedIn()

    log.info(LOADING_REQUEST)
    error = request.GET.get("error")
    submit_logout = INPUT_MAPPING.get("submit-logout", "submit-logout")
    submit_cancel = INPUT_MAPPING.get("submit-cancel", "submit-cancel")

    return LogoutContext(error=error, submit_logout=submit_logout, submit_cancel=submit_cancel)


async def get_register_page_context(request: HttpRequest) -> RegisterContext:
    """
    Get the context for the register page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        RegisterContext: The context for the register page.
    """
    log.info(CHECKING_USER_LOGGED_IN)
    user = await request.auser()
    if is_user_authenticated(user):
        log.warning(USER_ALREADY_LOGGED_IN)
        raise UserAlreadyLoggedIn()

    log.info(LOADING_REQUEST)
    error = request.GET.get("error")
    username_input = INPUT_MAPPING.get("username-input", "username-input")
    email_input = INPUT_MAPPING.get("email-input", "email-input")
    first_name_input = INPUT_MAPPING.get("first-name-input", "first-name-input")
    last_name_input = INPUT_MAPPING.get("last-name-input", "last-name-input")
    password_input = INPUT_MAPPING.get("password-input", "password-input")
    password_confirm_input = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")
    submit_register = INPUT_MAPPING.get("submit-register", "submit-register")

    return RegisterContext(
        error=error,
        username_input=username_input,
        email_input=email_input,
        first_name_input=first_name_input,
        last_name_input=last_name_input,
        password_input=password_input,
        password_confirm_input=password_confirm_input,
        submit_register=submit_register,
    )


async def login(request: HttpRequest) -> None:
    """
    Log in the user.

    Args:
        request (HttpRequest): The request object.
    """
    log.info(CHECKING_USER_LOGGED_IN)
    request_user = await request.auser()
    if is_user_authenticated(request_user):
        log.warning(USER_ALREADY_LOGGED_IN)
        raise UserAlreadyLoggedIn()

    log.info(LOADING_REQUEST)
    username_input = INPUT_MAPPING.get("username-input", "username-input")
    password_input = INPUT_MAPPING.get("password-input", "password-input")
    username = request.POST.get(username_input)
    password = request.POST.get(password_input)

    log.info("Authenticating user...")
    user = await aauthenticate(request=request, username=username, password=password)
    if user is None:
        log.warning("Invalid credentails.")
        raise InvalidCredentials()

    log.info("Logging user in...")
    await login_user(request, user)


async def logout(request: HttpRequest) -> None:
    """
    Log out the user.

    Args:
        request (HttpRequest): The request object.
    """
    log.info("Checking if user is logged out...")
    user = await request.auser()
    if not is_user_authenticated(user):
        log.warning("User is already logged out.")
        raise UserNotLoggedIn()

    log.info("Logging user out...")
    await logout_user(request)


async def register_user(request: HttpRequest) -> None:
    """
    Register a user.

    Args:
        request (HttpRequest): The request object.
    """
    log.info(CHECKING_USER_LOGGED_IN)
    user = await request.auser()
    is_authenticated = is_user_authenticated(user)
    if is_authenticated:
        log.warning(USER_ALREADY_LOGGED_IN)
        raise UserAlreadyLoggedIn()

    log.info("Loading Field IDs")
    username_input = INPUT_MAPPING.get("username-input", "username-input")
    email_input = INPUT_MAPPING.get("email-input", "email-input")
    first_name_input = INPUT_MAPPING.get("first-name-input", "first-name-input")
    last_name_input = INPUT_MAPPING.get("last-name-input", "last-name-input")
    password_input = INPUT_MAPPING.get("password-input", "password-input")
    password_confirm_input = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")

    log.info(LOADING_REQUEST)
    username = request.POST.get(username_input, None)
    email = request.POST.get(email_input)
    first_name = request.POST.get(first_name_input)
    last_name = request.POST.get(last_name_input)
    password = request.POST.get(password_input)
    password_confirmation = request.POST.get(password_confirm_input)

    log.info("Validating user details...")
    if not username or not email or not first_name or not last_name or not password:
        log.warning("Invalid user details.")
        raise InvalidUserDetails()
    elif await does_username_exist(username):
        log.warning("Invalid username.")
        raise UsernameAlreadyExists()
    elif await does_email_exist(email):
        log.warning("Invalid email.")
        raise EmailAlreadyExists()
    elif password != password_confirmation:
        log.warning("Passwords do not match.")
        raise NonMatchingCredentials()

    log.info("Creating user...")
    await create_user(username, password, first_name, last_name, email)
