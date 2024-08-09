"""Contains the models for the authentication app."""

import logging
from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import CASCADE, BooleanField, CharField, ForeignKey, Model

from authentication.errors.api_exceptions import ApiClientAlreadyRegistered

log = logging.getLogger(__name__)
log.info("Auth app models loading...")


class ApiClient(Model):
    """Model for an API client."""

    name = CharField(max_length=255)
    user = ForeignKey(User, on_delete=CASCADE)
    is_active = BooleanField(default=False)
    client_secret = CharField(max_length=255)

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return f"ApiClient for {self.user.username}"

    @classmethod
    async def enable_client(cls, user: User | AbstractBaseUser | AnonymousUser) -> str:
        """
        Enable a client.

        Args:
            user: The user to enable the client for.

        Returns:
            The client secret (Not accessible as plain text to the user after this).
        """
        client_secret = uuid4().hex

        if await cls.objects.filter(user=user).aexists():  # type: ignore
            raise ApiClientAlreadyRegistered()

        client = await cls.objects.acreate(
            name=f"{user.username}'s API Client",  # type: ignore
            user=user,
            is_active=True,
            client_secret=make_password(client_secret),
        )
        await client.asave()
        return client_secret

    @classmethod
    async def disable_client(cls, user: User | AbstractBaseUser | AnonymousUser) -> None:
        """
        Disable a client.

        Args:
            user: The user to disable the client for.
        """
        client = await cls.objects.aget(user=user)
        client.is_active = False
        await client.asave()


log.info("Auth app models loaded.")
