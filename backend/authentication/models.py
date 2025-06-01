"""Contains the models for the authentication app."""

import logging
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.core.cache import cache
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    FloatField,
    ForeignKey,
    Model,
)

log = logging.getLogger(__name__)


class ApiClient(Model):
    """Model for an API client."""

    user = ForeignKey(User, on_delete=CASCADE, db_index=True)
    is_active = BooleanField(default=True)
    client_secret = CharField(max_length=255, default="", blank=True)
    token = CharField(max_length=255, default="", blank=True, db_index=True, unique=True)
    token_expiration = FloatField(default=0)

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return f"ApiClient for {self.user.username}"

    async def get_token(self, user: User | AbstractBaseUser | AnonymousUser) -> tuple[str, str]:
        """
        Get a JWT token generated with the secret.

        Returns:
            tuple[str, str]: The token and its secret.
        """
        secret = uuid4().hex
        expiration = (datetime.now() + timedelta(minutes=5)).timestamp()
        jwt_token = jwt.encode(
            {
                "username": user.username,  # type: ignore
                "client_id": self.id,
                "exp": expiration,
            },
            secret,
            algorithm="HS256",
        )
        self.token = jwt_token
        self.token_expiration = expiration
        self.client_secret = secret
        await self.asave()
        await cache.aset(f"client_{user.id}", self, timeout=240)  # type: ignore
        return jwt_token, secret
