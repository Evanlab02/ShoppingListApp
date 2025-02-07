"""Contains the api user service repository."""

from django.contrib.auth import aauthenticate
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

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
from authentication.schemas.input import NewUser
from authentication.schemas.output import GeneralResponse
from authentication.services.interfaces.api.i_user_service import IUserService


class UserService(IUserService):
    """The user service."""

    def __init__(self, repo: IUserRepository = UserRepository()) -> None:
        """Initialize the user service."""
        self.repo = repo
        super().__init__()

    async def login(self, request: HttpRequest, username: str, password: str) -> GeneralResponse:
        """
        Login a user.

        Args:
            request (HttpRequest): The request.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            GeneralResponse: The general response.
        """
        request_user = await request.auser()
        if self.repo.is_user_authenticated(request_user):
            self.log.warning("User already logged in.")
            raise UserAlreadyLoggedIn()

        user = await aauthenticate(request=request, username=username, password=password)
        if user is None:
            self.log.warning("CRITICAL - Invalid credentials provided for user!")
            raise InvalidCredentials()

        await self.repo.login_user(request, user)
        return GeneralResponse(message="User successfully logged in.", detail="")

    async def logout(self, request: HttpRequest) -> GeneralResponse:
        """
        Logout a user.

        Args:
            request (HttpRequest): The request.

        Returns:
            GeneralResponse: The general response.
        """
        user = await request.auser()
        if not self.repo.is_user_authenticated(user):
            self.log.warning("User already logged out.")
            raise UserNotLoggedIn()

        await self.repo.logout_user(request)
        return GeneralResponse(message="User successfully logged out.", detail="")

    async def register_user(
        self, user: AnonymousUser | AbstractBaseUser | User, new_user: NewUser
    ) -> GeneralResponse:
        """
        Create a user.

        Args:
            request (HttpRequest): The request.
            new_user (NewUser): The new user.

        Returns:
            GeneralResponse: The general response.
        """
        is_authenticated = self.repo.is_user_authenticated(user)
        if is_authenticated:
            self.log.warning("User already logged in.")
            raise UserAlreadyLoggedIn()

        username = new_user.username
        password = new_user.password
        password_confirmation = new_user.password_confirmation
        first_name = new_user.first_name
        last_name = new_user.last_name
        email = new_user.email

        if not username or not email or not first_name or not last_name:
            self.log.warning("Invalid user details.")
            raise InvalidUserDetails()
        elif await self.repo.does_username_exist(username):
            self.log.warning("Invalid username.")
            raise UsernameAlreadyExists()
        elif await self.repo.does_email_exist(email):
            self.log.warning("Invalid email.")
            raise EmailAlreadyExists()
        elif password != password_confirmation:
            self.log.warning("Invalid credentials.")
            raise NonMatchingCredentials()

        await self.repo.create_user(username, password, first_name, last_name, email)
        return GeneralResponse(message="User successfully registered.", detail="")
