"""Contains the interfaces for the authentication view services."""

import logging
from abc import ABC, abstractmethod

from django.http import HttpRequest


class IUserService(ABC):
    """The user service interface."""

    def __init__(self) -> None:
        """Initialize the user service."""
        self.log = logging.getLogger(__name__)

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
