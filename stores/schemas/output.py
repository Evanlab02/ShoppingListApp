"""Contains outgoing data schemas for the stores app."""

from django.contrib.auth.models import User
from ninja import ModelSchema

from stores.models import ShoppingStore as Store


class UserSchema(ModelSchema):
    """User model schema for outgoing data."""

    class Meta:
        """Meta class for the UserSchema."""

        model = User
        fields = ["username"]


class StoreSchema(ModelSchema):
    """Store model schema for outgoing data."""

    user: UserSchema | None = None

    class Meta:
        """Meta class for the StoreSchema."""

        model = Store
        fields = [
            "id",
            "name",
            "store_type",
            "description",
            "created_at",
            "updated_at",
        ]
