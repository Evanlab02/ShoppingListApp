"""Contains the user repository for the authentication app."""

# Third party imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest


class UserRepository:
    """
    User repository for the authentication app.

    Methods:
        is_authenticated(user: User) -> bool
        create_user(payload: NewUser) -> User
        login_user(request: HttpRequest, payload: UserCredentials) -> (int, str)
        logout_user(request: HttpRequest) -> (int, str)
        render_or_redirect(Please view function for more information)
    """

    def is_authenticated(self, user: User) -> bool:
        """
        Check if a user is authenticated.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user is authenticated, otherwise False.
        """
        return user.is_authenticated

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        password_confirmation: str,
        first_name: str = "",
        last_name: str = "",
    ) -> User:
        """
        Register a user.

        Create a new user with the given credentials.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            password_confirmation (str): The password confirmation of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.

        Returns:
            (User): The created user.

        Raises:
            ValueError: If the username or email already exists or the passwords do not match.
        """
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists.")
        elif User.objects.filter(email=email).exists():
            raise ValueError("Email already exists.")
        elif password != password_confirmation:
            raise ValueError("Passwords do not match.")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        return user

    def login_user(self, request: HttpRequest, username: str, password: str) -> bool:
        """
        Login a user with the given credentials.

        Args:
            request (HttpRequest): The request object.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the user is authenticated, otherwise False.
        """
        user = authenticate(request=request, username=username, password=password)

        if user is None:
            return False

        login(request, user)

        return True

    def logout_user(self, request: HttpRequest) -> bool:
        """
        Logout a user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            bool: True if the user is was logged out, otherwise False.
        """
        if not self.is_authenticated(request.user):  # type: ignore
            return False

        logout(request)

        return True
