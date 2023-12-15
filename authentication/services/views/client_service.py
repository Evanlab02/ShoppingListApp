"""Contains the client service functions."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from authentication.database.client_repository import disable_for_user, enable_for_user
from authentication.database.user_repository import is_user_authenticated
from authentication.errors.api_exceptions import ApiClientAlreadyRegistered
from authentication.models import ApiClient
from authentication.schemas.contexts import BaseContext, TokenContext


async def enable_client(user: User | AbstractBaseUser | AnonymousUser) -> TokenContext:
    """Enable a client."""
    is_authenticated = await sync_to_async(is_user_authenticated)(user)
    if not is_authenticated:
        return TokenContext(error="User is not authenticated.")

    try:
        client_secret = await enable_for_user(user)
        return TokenContext(token=client_secret)
    except ApiClientAlreadyRegistered:
        return TokenContext(error="Client already registered.")


async def disable_client(user: User | AbstractBaseUser | AnonymousUser) -> BaseContext:
    """Disable a client."""
    is_authenticated = await sync_to_async(is_user_authenticated)(user)
    if not is_authenticated:
        return BaseContext(error="User is not authenticated.")

    try:
        await disable_for_user(user)
        return BaseContext()
    except ApiClient.DoesNotExist:
        return BaseContext(error="Client does not exist.")
