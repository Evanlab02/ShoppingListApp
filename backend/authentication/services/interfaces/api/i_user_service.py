"""Contains the api user service interface."""

import logging
from abc import ABC, abstractmethod

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.http import HttpRequest

from authentication.schemas.input import NewUser
from authentication.schemas.output import GeneralResponse

log = logging.getLogger(__name__)


class IUserService(ABC):
    """The user service interface."""

    def __init__(self) -> None:
        """Initialize the user service."""
        self.log = logging.getLogger(__name__)

    @abstractmethod
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

    @abstractmethod
    async def logout(self, request: HttpRequest) -> GeneralResponse:
        """
        Logout a user.

        Args:
            request (HttpRequest): The request.

        Returns:
            GeneralResponse: The general response.
        """

    @abstractmethod
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
