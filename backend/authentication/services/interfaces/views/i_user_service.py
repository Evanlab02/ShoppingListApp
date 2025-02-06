"""Contains the interfaces for the authentication view services."""

import logging
from abc import ABC, abstractmethod

from django.http import HttpRequest

from authentication.schemas.contexts import LoginContext, LogoutContext, RegisterContext


class IUserService(ABC):
    """The user service interface."""

    def __init__(self) -> None:
        """Initialize the user service."""
        self.log = logging.getLogger(__name__)

    @abstractmethod
    async def get_login_view_context(self, request: HttpRequest) -> LoginContext:
        """
        Generate context for the login view.

        Args:
            request (HttpRequest): The request object.

        Returns:
            LoginContext: The context for the login view.
        """

    @abstractmethod
    async def get_logout_view_context(self, request: HttpRequest) -> LogoutContext:
        """
        Generate context for the logout view.

        Args:
            request (HttpRequest): The request object.

        Returns:
            LogoutContext: The context for the logout view.
        """

    @abstractmethod
    async def get_register_page_context(self, request: HttpRequest) -> RegisterContext:
        """
        Get the context for the register page.

        Args:
            request (HttpRequest): The request object.

        Returns:
            RegisterContext: The context for the register page.
        """

    @abstractmethod
    async def login(self, request: HttpRequest) -> None:
        """
        Log in the user.

        Args:
            request (HttpRequest): The request object.
        """

    @abstractmethod
    async def logout(self, request: HttpRequest) -> None:
        """
        Log out the user.

        Args:
            request (HttpRequest): The request object.
        """

    @abstractmethod
    async def register_user(self, request: HttpRequest) -> None:
        """
        Register a user.

        Args:
            request (HttpRequest): The request object.
        """
