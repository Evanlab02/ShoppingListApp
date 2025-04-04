"""Contains the models for the stores app."""

import logging

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

from stores.constants import STORE_TYPE_CHOICES

log = logging.getLogger(__name__)


class ShoppingStore(Model):
    """Model for a shopping store."""

    name = CharField(max_length=100, unique=True, db_index=True)
    store_type = IntegerField(choices=STORE_TYPE_CHOICES, db_index=True)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    user = ForeignKey(User, on_delete=CASCADE, db_index=True)

    def __str__(self) -> str:
        """Return a string representation of the shopping store."""
        return f"{self.name}"

    async def auser(self) -> User:
        """Get the user for the store asynchronously."""
        func = sync_to_async(lambda: self.user)
        return await func()
