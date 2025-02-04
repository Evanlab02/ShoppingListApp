"""Contains the models for the authentication app."""

from datetime import timedelta, datetime
import logging
import jwt

from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import CASCADE, BooleanField, CharField, ForeignKey, Model, DateTimeField

from authentication.errors.api_exceptions import ApiClientAlreadyRegistered

log = logging.getLogger(__name__)
log.info("Auth app models loading...")


class ApiClient(Model):
    """Model for an API client."""

    name = CharField(max_length=255)
    user = ForeignKey(User, on_delete=CASCADE)
    is_active = BooleanField(default=False)
    client_secret = CharField(max_length=255)
    token = CharField(max_length=255, null=True, blank=True)
    token_expiration = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return f"ApiClient for {self.user.username}"

    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser, secret: str) -> str:
        """
        Get a JWT token generated with the secret.

        Args:
            secret: The secret of the client.

        Returns:
            str: The token
        """
        expiration = datetime.now() + timedelta(minutes=5)
        jwt_token = jwt.encode(
            {
                "username": user.username,
                "client_id": self.id,
                "exp": expiration,
            },
            secret,
            algorithm="HS256",
        )
        self.token = jwt_token
        self.token_expiration = expiration
        await self.asave()
        return jwt_token

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

        if await cls.objects.filter(user=user).aexists():
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
