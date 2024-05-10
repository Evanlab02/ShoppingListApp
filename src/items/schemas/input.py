"""Contains schemas that are incoming from the user."""

from ninja import Schema


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
