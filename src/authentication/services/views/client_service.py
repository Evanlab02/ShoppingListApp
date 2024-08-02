"""Contains the client service functions."""

import logging

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database.client_repository import disable_for_user, enable_for_user
from authentication.database.user_repository import is_user_authenticated
from authentication.errors.api_exceptions import ApiClientAlreadyRegistered
from authentication.models import ApiClient
from authentication.schemas.contexts import BaseContext, TokenContext

log = logging.getLogger(__name__)
log.info("Authentication View client service loading...")

USER_IS_NOT_AUTHENTICATED = "User is not authenticated."


async def enable_client(user: User | AbstractBaseUser | AnonymousUser) -> TokenContext:
    """Enable a client."""
    log.info("Checking if user is logged in...")
    is_authenticated = await sync_to_async(is_user_authenticated)(user)
    if not is_authenticated:
        log.warning(USER_IS_NOT_AUTHENTICATED)
        return TokenContext(error=USER_IS_NOT_AUTHENTICATED)

    try:
        log.info("Enabling user client...")
        client_secret = await enable_for_user(user)
        return TokenContext(token=client_secret)
    except ApiClientAlreadyRegistered:
        log.info("User client already registered.")
        return TokenContext(error="Client already registered.")


async def disable_client(user: User | AbstractBaseUser | AnonymousUser) -> BaseContext:
    """Disable a client."""
    log.info("Checking if user is logged in...")
    is_authenticated = await sync_to_async(is_user_authenticated)(user)
    if not is_authenticated:
        log.warning(USER_IS_NOT_AUTHENTICATED)
        return BaseContext(error=USER_IS_NOT_AUTHENTICATED)

    try:
        log.info("Disabling user client...")
        await disable_for_user(user)
        return BaseContext()
    except ApiClient.DoesNotExist:
        log.info("User client does not exist.")
        return BaseContext(error="Client does not exist.")


log.info("Authentication View client service loaded.")
