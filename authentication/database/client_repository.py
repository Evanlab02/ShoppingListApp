"""Contains the client repository functions."""

from ..models import Client


async def get_client_by_user_id(user_id: int) -> Client:
    """Get the client associated with the given user.

    Args:
        user_id (int): The user id.

    Returns:
        Client: The client.

    Raises:
        Client.DoesNotExist: If the client does not exist.
    """
    client = await Client.objects.aget(user_id=user_id)
    return client
