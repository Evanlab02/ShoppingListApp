"""Contains schemas that are outgoing to the user."""

from ninja import ModelSchema

from items.models import ShoppingItem as Item
from shoppingapp.schemas.shared import UserSchema
from stores.schemas.output import StoreSchemaNoUser


class ItemSchema(ModelSchema):
    """Item model schema for outgoing data."""

    user: UserSchema | None = None
    store: StoreSchemaNoUser | None = None

    class Meta:
        """Meta class for the ItemSchema."""

        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "created_at",
            "updated_at",
        ]
