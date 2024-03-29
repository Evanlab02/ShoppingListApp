"""Contains contexts for the rendering in the items app."""

from items.schemas.output import ItemPaginationSchema
from shoppingapp.schemas.shared import BaseContext
from stores.schemas.output import StoreSchema


class ItemCreateContext(BaseContext):
    """Item create context."""

    stores: list[StoreSchema]


class ItemOverviewContext(BaseContext):
    """Item overview context."""

    pagination: ItemPaginationSchema
