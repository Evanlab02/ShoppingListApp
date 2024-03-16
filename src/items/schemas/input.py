"""Contains schemas that are incoming from the user."""

from ninja import Schema


class NewItem(Schema):
    """New Item Schema."""

    store_id: int
    name: str
    price: float
    description: str = ""
