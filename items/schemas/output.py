"""Contains schemas that are outgoing to the user."""

from ninja import ModelSchema, Schema

from items.models import ShoppingItem as Item
from shoppingapp.schemas.shared import PaginationSchema, UserSchema
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


class ItemPaginationSchema(PaginationSchema):
    """Pagination schema for outgoing data."""

    items: list[ItemSchema] = []


class ItemAggregationSchema(Schema):
    """Aggregation schema for outgoing data."""

    total_items: int | None = None
    total_price: float | None = None
    average_price: float | None = None
    max_price: float | None = None
    min_price: float | None = None
