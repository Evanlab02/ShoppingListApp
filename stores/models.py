"""Contains the models for the stores app."""

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


class ShoppingStore(Model):
    """Model for a shopping store."""

    name = CharField(max_length=100, unique=True)
    store_type = IntegerField(choices=STORE_TYPE_CHOICES)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the shopping store."""
        return f"{self.name}"
