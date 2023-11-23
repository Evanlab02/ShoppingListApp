"""Contains the client repository."""

# Third party imports
from django.contrib.auth.models import User

# Local application imports
from ..models import Client


class ClientRepository:
    """
    Client repository.

    Methods:
        get_client(user: User) -> Client | None
        generate_token(user: User) -> str
    """

    def get_client(self, user: User) -> Client | None:
        """
        Get a client if it exists, otherwise return None.

        Args:
            user (User): The user to get the client for.

        Returns:
            Client | None: The client if it exists, otherwise None.
        """
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            client = None
        return client

    def generate_token(self, user: User) -> str:
        """
        Generate a token for a user.

        Args:
            user (User): The user to generate the token for.

        Returns:
            str: The generated token.
        """
        client = None

        # Attempt to get client
        try:
            client = Client.objects.filter(user=user).get()
        except Client.DoesNotExist:
            client = None

        # If client does not exist, create it
        if client is None:
            client = Client.objects.create(user=user)
            client.save()

        # Generate token for client
        client.generate_token()

        # Return client token
        return client.token
