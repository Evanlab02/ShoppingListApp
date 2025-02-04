"""Contains the api user service functions."""

import logging

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database import client_repository as repo

log = logging.getLogger(__name__)

async def get_token(user: User | AbstractBaseUser | AnonymousUser, secret: str) -> str:
    """
    Get a token.

    Args:
        secret: The secret of the client

    Returns:
        str: The token
    """
    return await repo.get_token(user, secret)
