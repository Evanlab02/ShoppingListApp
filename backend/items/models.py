"""Contains the models for the items app."""

import logging

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    Model,
    TextField,
)

from stores.models import ShoppingStore as Store

log = logging.getLogger(__name__)


class ShoppingItem(Model):
    """Model for a shopping item."""

    name = CharField(max_length=100)
    description = TextField(blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    store = ForeignKey(Store, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the shopping item."""
        return f"{self.name}@{self.store.name}"

    async def astore(self) -> Store:
        """Get the store for the item asynchronously."""
        func = sync_to_async(lambda: self.store)
        return await func()

    async def auser(self) -> User:
        """Get the user for the item asynchronously."""
        func = sync_to_async(lambda: self.user)
        return await func()
