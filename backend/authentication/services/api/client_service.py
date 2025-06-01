"""Contains the api user service functions."""

import logging

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database.client_repo import ClientRepository
from authentication.services.interfaces.api.i_client_service import IClientService

log = logging.getLogger(__name__)


class ClientService(IClientService):
    """The client service."""

    def __init__(self) -> None:
        """Initialize the client service."""
        self.repo = ClientRepository()
        super().__init__()

    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
        """
        Get a token and its secret.

        Args:
            user: The user to get the token for.

        Returns:
            tuple[str, str]: The token and its secret.
        """
        return await self.repo.get_token(user)
