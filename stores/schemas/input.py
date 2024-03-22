"""Contains incoming data schemas for the stores app."""

from ninja import Schema


class NewStore(Schema):
    """New store schema for incoming data."""

    name: str
    store_type: str | int
    description: str


class StoreDescription(Schema):
    """Store description schema used in the update endpoint."""

    description: str | None = None
