"""Contains outgoing data schemas for the stores app."""

from ninja import ModelSchema

from stores.models import ShoppingStore as Store


class StoreSchema(ModelSchema):
    """Store model schema for outgoing data."""

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
