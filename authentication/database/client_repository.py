"""Contains the client repository functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from ..models import Client


async def get_client_by_user(
    user: int | AbstractBaseUser | AnonymousUser | User,
) -> Client:
    """
    Get the client associated with the given user.

    Args:
        user (int | AbstractBaseUser | AnonymousUser | User): The user.

    Returns:
        Client: The client.

    Raises:
        Client.DoesNotExist: If the client does not exist.
    """
    client = await Client.objects.aget(user=user)
    return client


async def generate_token(user: AbstractBaseUser | AnonymousUser | User) -> str:
    """
    Generate a new token for the given user.

    Args:
        user_id (int): The user id.

    Returns:
        str: The token.
    """
    client = None

    try:
        client = await get_client_by_user(user)
        await client.generate_token()
    except Client.DoesNotExist:
        client = await Client.objects.acreate(user=user)
        await client.asave()
        await client.generate_token()

    token = await client.get_token()
    return token
