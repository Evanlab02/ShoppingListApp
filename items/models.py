"""Contains the models for the items app."""

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)

from stores.models import ShoppingStore as Store


class ShoppingItem(Model):
    """Model for a shopping item."""

    name = CharField(max_length=100)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    store = ForeignKey(Store, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the shopping item."""
        return f"{self.name}@{self.store.name}"
