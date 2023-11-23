"""Contains the API key authentication helper class."""

# Third party imports
from django.http import HttpRequest
from ninja.security import APIKeyHeader

# Local application imports
from ..constants import API_KEY_PARAM
from ..database import ClientRepository, UserRepository
from ..models import Client

# Database repositories
CLIENT_REPO = ClientRepository()
USER_REPO = UserRepository()


class ApiKey(APIKeyHeader):
    """
    API key authentication helper class.

    Attributes:
        param_name (str): The name of the header parameter.

    Methods:
        authenticate(request: HttpRequest, key: str) -> Client | None
    """

    param_name = API_KEY_PARAM

    def authenticate(self, request: HttpRequest, key: str | None) -> Client | None:
        """
        Authenticate a user.

        Args:
            request (HttpRequest): The request to authenticate.
            key (str): The key to authenticate with.

        Returns:
            Client | None: The client if the authentication was successful, otherwise None.
        """
        # Check if user is authenticated, if not return None (Fail)
        if not USER_REPO.is_authenticated(request.user):  # type: ignore
            return None

        # Get client related to user
        client = CLIENT_REPO.get_client(request.user)  # type: ignore

        # If Client does not exist or key is empty string, return None (Fail)
        if client is None or key == "":
            return None
        # If key matches client token, return client (Pass)
        elif key == client.token:
            return client

        return None
