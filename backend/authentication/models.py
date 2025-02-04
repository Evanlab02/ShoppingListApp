"""Contains the models for the authentication app."""

import logging
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
)

log = logging.getLogger(__name__)


class ApiClient(Model):
    """Model for an API client."""

    user = ForeignKey(User, on_delete=CASCADE, db_index=True)
    is_active = BooleanField(default=True)
    client_secret = CharField(max_length=255, default=None, null=True, blank=True)
    token = CharField(max_length=255, null=True, blank=True, db_index=True)
    token_expiration = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return f"ApiClient for {self.user.username}"

    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
        """
        Get a JWT token generated with the secret.

        Args:
            secret: The secret of the client.

        Returns:
            str: The token
        """
        if self.client_secret is None:
            self.client_secret = uuid4().hex
            await self.asave()

        expiration = datetime.now() + timedelta(minutes=5)
        jwt_token = jwt.encode(
            {
                "username": user.username,  # type: ignore
                "client_id": self.id,
                "exp": expiration,
            },
            self.client_secret,
            algorithm="HS256",
        )
        self.token = jwt_token
        self.token_expiration = expiration
        await self.asave()
        return jwt_token, self.client_secret
