"""Contains outgoing data schemas for the stores app."""

from ninja import ModelSchema, Schema

from shoppingapp.schemas.shared import UserSchema
from stores.models import ShoppingStore as Store


class StoreSchemaNoUser(ModelSchema):
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


class StoreAggregationSchema(Schema):
    """Store aggregation schema for outgoing data."""

    total_stores: int = 0
    online_stores: int = 0
    in_store_stores: int = 0
    combined_stores: int = 0
    combined_online_stores: int = 0
    combined_in_store_stores: int = 0


class StorePaginationSchema(Schema):
    """Pagination schema for outgoing data."""

    total: int = 0
    page_number: int = 1
    total_pages: int = 1
    has_previous: bool = False
    previous_page: int | None = None
    has_next: bool = False
    next_page: int | None = None
    stores: list[StoreSchema] = []
