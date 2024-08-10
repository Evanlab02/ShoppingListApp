"""Contains schemas that are incoming from the user."""

import logging
from datetime import date

from ninja import Schema

log = logging.getLogger(__name__)
log.info("Item input schemas loading...")


class NewItem(Schema):
    """New Item Schema."""

    store_id: int
    name: str
    price: float
    description: str = ""


class UpdateItem(Schema):
    """Update Item Schema."""

    store_id: int | None = None
    name: str | None = None
    price: float | None = None
    description: str | None = None


class ItemSearchSchema(Schema):
    """Schema used to search items."""

    ids: list[int] | None = None
    stores: list[int] | None = None
    created_on: date | None = None
    created_before: date | None = None
    created_after: date | None = None
    updated_on: date | None = None
    updated_before: date | None = None
    updated_after: date | None = None
    description: str | None = None
    price: float | None = None
    price_is_lt: float | None = None
    price_is_gt: float | None = None


log.info("Item input schemas loaded.")
