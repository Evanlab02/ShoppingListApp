"""Contains the UserRepository class."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


class UserRepository:
    """
    The user repository to interact with User objects.

    Methods:
        is_user_authenticated(user): Check if the user is authenticated.
    """

    def is_user_authenticated(self, user: AbstractBaseUser | AnonymousUser) -> bool:
        """
        Check if the user is authenticated.

        Args:
            user (AbstractBaseUser | AnonymousUser): The user to check.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        authenticated = user.is_authenticated
        return authenticated
