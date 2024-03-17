"""Contains contexts for the rendering in the items app."""

from shoppingapp.schemas.shared import BaseContext
from stores.schemas.output import StoreSchema


class ItemCreateContext(BaseContext):
    """Item create context."""

    stores: list[StoreSchema]
