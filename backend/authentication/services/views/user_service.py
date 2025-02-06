"""Contains the user view service."""

from django.contrib.auth import aauthenticate
from django.http import HttpRequest

from authentication.constants import INPUT_MAPPING
from authentication.database.interfaces.i_user_repo import IUserRepository
from authentication.database.user_repo import UserRepository
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
from authentication.services.interfaces.views.i_user_service import IUserService


class UserService(IUserService):
    """The user service."""

    def __init__(self, repo: IUserRepository = UserRepository()) -> None:
        """Initialize the user service."""
        self.repo = repo
        super().__init__()

    async def get_login_view_context(self, request: HttpRequest) -> LoginContext:
        """
        Generate context for the login view.

        Args:
            request (HttpRequest): The request object.

        Returns:
            LoginContext: The context for the login view.
        """
        user = await request.auser()
        if self.repo.is_user_authenticated(user):
            self.log.warning("Duplicate login request.")
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

    async def get_logout_view_context(self, request: HttpRequest) -> LogoutContext:
        """
        Generate context for the logout view.

        Args:
            request (HttpRequest): The request object.

        Returns:
            LogoutContext: The context for the logout view.
        """
        user = await request.auser()
        if not self.repo.is_user_authenticated(user):
            self.log.warning("User is not logged in.")
            raise UserNotLoggedIn()

        error = request.GET.get("error")
        submit_logout = INPUT_MAPPING.get("submit-logout", "submit-logout")
        submit_cancel = INPUT_MAPPING.get("submit-cancel", "submit-cancel")

        return LogoutContext(error=error, submit_logout=submit_logout, submit_cancel=submit_cancel)

    async def get_register_page_context(self, request: HttpRequest) -> RegisterContext:
        """
        Get the context for the register page.

        Args:
            request (HttpRequest): The request object.

        Returns:
            RegisterContext: The context for the register page.
        """
        user = await request.auser()
        if self.repo.is_user_authenticated(user):
            self.log.warning("Attempting to register while logged in.")
            raise UserAlreadyLoggedIn()

        error = request.GET.get("error")
        username_input = INPUT_MAPPING.get("username-input", "username-input")
        email_input = INPUT_MAPPING.get("email-input", "email-input")
        first_name_input = INPUT_MAPPING.get("first-name-input", "first-name-input")
        last_name_input = INPUT_MAPPING.get("last-name-input", "last-name-input")
        password_input = INPUT_MAPPING.get("password-input", "password-input")
        password_confirm_input = INPUT_MAPPING.get(
            "password-confirm-input", "password-confirm-input"
        )
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

    async def login(self, request: HttpRequest) -> None:
        """
        Log in the user.

        Args:
            request (HttpRequest): The request object.
        """
        request_user = await request.auser()
        if self.repo.is_user_authenticated(request_user):
            self.log.warning("Attempting to login while already logged in.")
            raise UserAlreadyLoggedIn()

        username_input = INPUT_MAPPING.get("username-input", "username-input")
        password_input = INPUT_MAPPING.get("password-input", "password-input")
        username = request.POST.get(username_input)
        password = request.POST.get(password_input)

        user = await aauthenticate(request=request, username=username, password=password)
        if user is None:
            self.log.warning("Invalid credentials.")
            raise InvalidCredentials()

        await self.repo.login_user(request, user)

    async def logout(self, request: HttpRequest) -> None:
        """
        Log out the user.

        Args:
            request (HttpRequest): The request object.
        """
        user = await request.auser()
        if not self.repo.is_user_authenticated(user):
            self.log.warning("User is already logged out.")
            raise UserNotLoggedIn()

        await self.repo.logout_user(request)

    async def register_user(self, request: HttpRequest) -> None:
        """
        Register a user.

        Args:
            request (HttpRequest): The request object.
        """
        user = await request.auser()
        if self.repo.is_user_authenticated(user):
            self.log.warning("Attempting to register while logged in.")
            raise UserAlreadyLoggedIn()

        username_input = INPUT_MAPPING.get("username-input", "username-input")
        email_input = INPUT_MAPPING.get("email-input", "email-input")
        first_name_input = INPUT_MAPPING.get("first-name-input", "first-name-input")
        last_name_input = INPUT_MAPPING.get("last-name-input", "last-name-input")
        password_input = INPUT_MAPPING.get("password-input", "password-input")
        password_confirm_input = INPUT_MAPPING.get(
            "password-confirm-input", "password-confirm-input"
        )

        username = request.POST.get(username_input, None)
        email = request.POST.get(email_input)
        first_name = request.POST.get(first_name_input)
        last_name = request.POST.get(last_name_input)
        password = request.POST.get(password_input)
        password_confirmation = request.POST.get(password_confirm_input)

        if not username or not email or not first_name or not last_name or not password:
            self.log.warning("Invalid user details.")
            raise InvalidUserDetails()
        elif await self.repo.does_username_exist(username):
            self.log.warning("Invalid username.")
            raise UsernameAlreadyExists()
        elif await self.repo.does_email_exist(email):
            self.log.warning("Invalid email.")
            raise EmailAlreadyExists()
        elif password != password_confirmation:
            self.log.warning("Passwords do not match.")
            raise NonMatchingCredentials()

        await self.repo.create_user(username, password, first_name, last_name, email)
