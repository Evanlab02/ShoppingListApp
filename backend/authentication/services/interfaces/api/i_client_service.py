"""Contains the api client service interface."""

import logging
from abc import ABC, abstractmethod

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

log = logging.getLogger(__name__)


class IClientService(ABC):
    """The client service interface."""

    def __init__(self) -> None:
        """Initialize the client service."""
        self.log = logging.getLogger(__name__)

    @abstractmethod
    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
        """
        Get a token and its secret.

        Args:
            user: The user to get the token for.

        Returns:
            tuple[str, str]: The token and its secret.
        """
