"""Contains outgoing data schemas for the stores app."""

from ninja import ModelSchema

from stores.models import ShoppingStore as Store


class StoreSchema(ModelSchema):
    """Store model schema for outgoing data."""

    store_type: str

    class Meta:
        """Meta class for the StoreSchema."""

        model = Store
        exclude = ["id", "created_at", "updated_at", "user", "store_type"]
