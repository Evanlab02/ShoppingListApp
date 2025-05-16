"""Contains the user view service."""

from django.contrib.auth import aauthenticate
from django.http import HttpRequest

from authentication.database.interfaces.i_user_repo import IUserRepository
from authentication.database.user_repo import UserRepository
from authentication.errors.exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.services.interfaces.views.i_user_service import IUserService


class UserService(IUserService):
    """The user service."""

    def __init__(self, repo: IUserRepository = UserRepository()) -> None:
        """Initialize the user service."""
        self.repo = repo
        super().__init__()

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

        username = request.POST.get("username")
        password = request.POST.get("password")

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

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if not username or not email or not first_name or not last_name or not password:
            self.log.warning("Invalid user details.")
            raise InvalidUserDetails()
        elif await self.repo.does_username_exist(username):
            self.log.warning("Invalid username.")
            raise UsernameAlreadyExists()
        elif await self.repo.does_email_exist(email):
            self.log.warning("Invalid email.")
            raise EmailAlreadyExists()
        elif password != password_confirm:
            self.log.warning("Passwords do not match.")
            raise NonMatchingCredentials()

        await self.repo.create_user(username, password, first_name, last_name, email)
