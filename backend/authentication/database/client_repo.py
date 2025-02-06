"""Contains the client repository."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database.interfaces.i_client_repo import IClientRepository
from authentication.models import ApiClient


class ClientRepository(IClientRepository):
    """The client repository."""

    def __init__(self) -> None:
        """Initialize the client repository."""
        super().__init__()

    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
        """
        Get a token and its secret.

        Args:
            user: The user to get the token for.

        Returns:
            tuple[str, str]: The token and its secret.
        """
        client, _ = await ApiClient.objects.aget_or_create(user=user)
        return await client.get_token(user)
