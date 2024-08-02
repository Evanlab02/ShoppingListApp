"""Contains the client repository functions."""

import logging

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.models import ApiClient

log = logging.getLogger(__name__)
log.info("Loading client repository...")


async def enable_for_user(user: User | AbstractBaseUser | AnonymousUser) -> str:
    """Enable a client."""
    client_secret = await ApiClient.enable_client(user)
    return client_secret


async def disable_for_user(user: User | AbstractBaseUser | AnonymousUser) -> None:
    """Disable a client."""
    await ApiClient.disable_client(user)


log.info("Loaded client repository.")
