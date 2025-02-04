"""Contains the client repository functions."""

import logging

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.models import ApiClient

log = logging.getLogger(__name__)


async def get_token(user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
    """
    Get a token.

    Args:
        user: The user to get the token for.

    Returns:
        The JWT token.
    """
    client, _ = await ApiClient.objects.aget_or_create(user=user)
    return await client.get_token(user)
