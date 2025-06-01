"""Contains the user repository functions."""

from django.contrib.auth import alogin, alogout
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

from authentication.database.interfaces.i_user_repo import IUserRepository


class UserRepository(IUserRepository):
    """The user repository."""

    def __init__(self) -> None:
        """Initialize the user repository."""
        super().__init__()

    async def create_user(
        self,
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

    async def does_email_exist(self, email: str) -> bool:
        """
        Check if a email exists.

        Args:
            email (str): The email of the user.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        return await User.objects.filter(email=email).aexists()

    async def does_username_exist(self, username: str) -> bool:
        """
        Check if a username exists.

        Args:
            username (str): The username of the user.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        return await User.objects.filter(username=username).aexists()

    def is_user_authenticated(self, user: AbstractBaseUser | AnonymousUser | User) -> bool:
        """
        Check if the user is authenticated.

        Args:
            user (AbstractBaseUser | AnonymousUser | User): The user to check.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return user.is_authenticated

    async def login_user(self, request: HttpRequest, user: User) -> None:
        """
        Login a user.

        Args:
            request (HttpRequest): The request.
            user (User): The user to login.
        """
        await alogin(request, user)

    async def logout_user(self, request: HttpRequest) -> None:
        """
        Logout a user.

        Args:
            request (HttpRequest): The request.
        """
        await alogout(request)
